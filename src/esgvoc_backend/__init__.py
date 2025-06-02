import logging
import logging.config

__version__ = "0.4.0.post0"

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'esgvoc_backend_formatter': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s: %(message)s',
        }
    },
    'handlers': {
        'esgvoc_backend_stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'esgvoc_backend_formatter',
        }
    },
    'loggers': {
        'esgvoc_backend': {
            'handlers': ['esgvoc_backend_stdout'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

logging.config.dictConfig(logging_config)
