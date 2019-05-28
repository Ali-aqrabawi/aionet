import re

from aionet.vendors.devices.base import BaseDevice


class Terminal(BaseDevice):
    """Class for working with General Terminal"""

    def __init__(self, delimeter_list=None, *args, **kwargs):
        """
        Initialize class for asynchronous working with network devices
        Invoke init with some special params (base_pattern and username)

        :param str host: device hostname or ip address for connection
        :param str username: username for logging to device
        :param str password: user password for logging to device
        :param int port: ssh port for connection. Default is 22
        :param str device_type: network device type
        :param known_hosts: file with known hosts. Default is None (no policy). With () it will use default file
        :param delimeter_list: list with delimeters
        :param str local_addr: local address for binding source of tcp connection
        :param client_keys: path for client keys. Default in None. With () it will use default file in OS
        :param str passphrase: password for encrypted client keys
        :param float timeout: timeout in second for getting information from channel
        :param loop: asyncio loop object
        """
        super().__init__(*args, **kwargs)
        if delimeter_list is not None:
            self._delimiter_list = delimeter_list

    _delimiter_list = ["$", "#"]
    """All this characters will stop reading from buffer. It mean the end of device prompt"""

    _pattern = r"[{delimiters}]"
    """Pattern for using in reading buffer. When it found processing ends"""

    async def _set_base_prompt(self):
        """Setting base pattern"""
        self._logger.info("Host {}: Setting base prompt".format(self.host))
        delimiters = map(re.escape, type(self)._delimiter_list)
        delimiters = r"|".join(delimiters)
        pattern = type(self)._pattern
        base_pattern = pattern.format(delimiters=delimiters)
        self._logger.debug("Host {}: Base Pattern: {}".format(self.host, base_pattern))
        self._conn.set_base_pattern(base_pattern)
