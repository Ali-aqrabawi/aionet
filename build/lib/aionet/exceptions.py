class BaseAionetError(Exception):
    _error_name = ''

    def __init__(self, ip_address, code, reason):
        self.ip_address = ip_address
        self.code = code
        self.reason = reason
        self.msg = "Host %s %s Error: %s" % (ip_address, type(self)._error_name, reason)
        super().__init__(self.msg)


class AionetAuthenticationError(BaseAionetError):
    _error_name = 'Authentication'


class AionetTimeoutError(BaseAionetError):
    _error_name = 'timeout'


class AionetCommitError(BaseAionetError):
    _error_name = 'commit'


class AionetConnectionError(BaseAionetError):
    _error_name = 'connection'
