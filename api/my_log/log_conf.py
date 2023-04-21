CONFIG_PROD = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "activity": {
            "format": "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "my_log/warns.txt",
            "maxBytes": 5000
        },
        "access": {
            "formatter": "access",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": "my_log/access.txt",
            "maxBytes": 5000
        },
        "activity": {
            "formatter": "activity",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": "my_log/log_activity.txt",
            "maxBytes": 5000
        }
    },
    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["access"],
            "propagate": False
        },
        "activity": {
            "level": "INFO",
            "handlers": ["activity"],
            "propagate": False
        }
    }
}

DEBUG_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'activity': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}