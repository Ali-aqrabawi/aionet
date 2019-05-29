class AionetAuthenticationError(Exception):

    def __init__(self, ip_address, code, reason):
        self.ip_address = ip_address
        self.code = code
        self.reason = reason
        self.msg = "Host %s Disconnect Error: %s" % (ip_address, reason)
        super().__init__(self.msg)


class AionetTimeoutError(Exception):

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.msg = "Host %s Timeout Error" % (ip_address)
        super().__init__(self.msg)


class AionetCommitError(Exception):

    def __init__(self, ip_address, reason):
        self.ip_address = ip_address
        self.reason = reason
        self.msg = "Host %s Commit Error: %s" % (ip_address, reason)
        super().__init__(self.msg)
