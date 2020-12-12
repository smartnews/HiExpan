logging_conf = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 500,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': False,
            'filename': 'logs/concurrent.log',
            'formatter': 'verbose'
        },
        'errfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': False,
            'filename': 'logs/error.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'errfile', 'console'],
            'level': 'INFO',
        },
        'tornado': {
            'handlers': ['file', 'errfile'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
