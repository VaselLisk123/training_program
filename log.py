import logging
from logging import config
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '[%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'filename': "shopify.log"
        },
    },
    'loggers': {
        'shopify_logger': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

def create_logger():
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("shopify_logger")
    return logger