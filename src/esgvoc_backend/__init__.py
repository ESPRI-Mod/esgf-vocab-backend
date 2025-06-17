import logging
import logging.config

from esgvoc_backend import constants

__version__ = "0.4.0.post3"

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'esgvoc_backend_formatter': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s: %(message)s',
        },
        'gunicorn_formatter': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s] Gunicorn - %(message)s',
        }
    },
    'handlers': {
        'esgvoc_backend_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'esgvoc_backend_formatter',
        },
        'gunicorn_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'gunicorn_formatter',
        }
    },
    'loggers': {
        'esgvoc_backend': {
            'handlers': ['esgvoc_backend_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.access': {
            'handlers': ['gunicorn_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn.error': {
            'handlers': ['gunicorn_handler'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

logging.config.dictConfig(logging_config)

# Configure the ESGVOC library logger.
logging.getLogger(constants.ESGVOC_ROOT_LOGGER_NAME).setLevel(constants.LOG_LEVEL)
