import logging
from json import dumps

import structlog
from structlog import WriteLoggerFactory

from config_reader import LogRenderer, Settings


def get_structlog_config(settings: Settings) -> dict:
    return {
        "processors": get_processors(settings),
        "cache_logger_on_first_use": True,
        "wrapper_class": structlog.make_filtering_bound_logger(settings.log.level),
        "logger_factory": WriteLoggerFactory()
    }


def get_processors(settings: Settings) -> list:
    def custom_json_serializer(data, *args, **kwargs):
        """
        JSON-objects custom serializer
        """
        result = {}
        data = dict(data.items())

        if settings.log.show_datetime and 'timestamp' in data:
            result['timestamp'] = data.pop('timestamp')

        for key in ('level', 'event'):
            value = data.pop(key, None)
            if value is not None:
                result[key] = value

        result.update(data)
        return dumps(result, default=str)

    processors = [
        # Context vars должен быть первым
        structlog.contextvars.merge_contextvars,

        # Обработка исключений (исправлено здесь)
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,  # Убраны скобки!

        # Таймстампер (только если включен)
        *([structlog.processors.TimeStamper(fmt=settings.log.datetime_format)]
          if settings.log.show_datetime else []),

        structlog.processors.add_log_level,
        structlog.processors.UnicodeDecoder()
    ]

    if settings.log.renderer == LogRenderer.JSON:
        processors.append(structlog.processors.JSONRenderer(
            serializer=custom_json_serializer
        ))
    else:
        processors.append(structlog.dev.ConsoleRenderer(
            colors=settings.log.use_colors_in_console,
            pad_level=True
        ))

    return processors
