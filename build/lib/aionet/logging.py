"""
Logging Module
"""
import logging


class aionetLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra):
        super(aionetLoggerAdapter, self).__init__(logger, extra)

    def process(self, msg, kwargs):
        msg, kwargs = super(aionetLoggerAdapter, self).process(msg, kwargs)
        msg = 'Host %s: ' % kwargs['extra']['host'] + msg
        return msg, {}


logger = logging.getLogger(__package__)
logger.setLevel(logging.WARNING)
