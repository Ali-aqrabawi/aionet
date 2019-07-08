"""Subclass specific to Cisco ASA"""

from aionet.vendors.devices.base_ios import BaseIOSDevice


class CiscoASA(BaseIOSDevice):
    """Class for working with Cisco ASA"""

    def __init__(self, *args, **kwargs):
        """
        Initialize class for asynchronous working with network devices

        :param str host: device hostname or ip address for connection
        :param str username: username for logging to device
        :param str password: user password for logging to device
        :param str secret: secret password for privilege mode
        :param int port: ssh port for connection. Default is 22
        :param str device_type: network device type
        :param known_hosts: file with known hosts. Default is None (no policy). With () it will use default file
        :param str local_addr: local address for binding source of tcp connection
        :param client_keys: path for client keys. Default in None. With () it will use default file in OS
        :param str passphrase: password for encrypted client keys
        :param float timeout: timeout in second for getting information from channel
        :param loop: asyncio loop object
        """
        super().__init__(*args, **kwargs)
        self._multiple_mode = False

    _disable_paging_command = "terminal pager 0"

    @property
    def multiple_mode(self):
        """ Returning Bool True if ASA in multiple mode"""
        return self._multiple_mode

    async def _session_preparation(self):
        await super()._session_preparation()
        await self._check_multiple_mode()

    async def _disable_width(self):
        self._logger.info("setting terminal width to 511")
        await self.send_config_set([type(self)._disable_width_command])

    async def _check_multiple_mode(self):
        """Check mode multiple. If mode is multiple we adding info about contexts"""
        self._logger.info("Checking multiple mode")
        out = await self.send_command_expect("show mode")
        if "multiple" in out:
            self._multiple_mode = True

        self._logger.debug("Multiple mode: %s" % self._multiple_mode)
