from logging import config as logging_config


DEBUG = True

DATABASE = {
    'user': 'rschweppes',
    'password': '',
    'host': '127.0.0.1',
    'database': 'megadb',
    'port': '5432',
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'aiopg': {
            'propagate': DEBUG,
        },
    }
}

logging_config.dictConfig(LOGGING)
