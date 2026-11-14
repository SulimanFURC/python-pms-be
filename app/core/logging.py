import logging
import logging.config


def setup_logging() -> None:
    """Configure application-wide logging."""

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": ("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": "INFO",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            },
        }
    )
