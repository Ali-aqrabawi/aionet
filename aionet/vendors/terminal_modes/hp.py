"""
Hp Terminal Modes
"""
from aionet.logging import logger
from aionet.vendors.terminal_modes.base import BaseTerminalMode


class SystemView(BaseTerminalMode):
    """ System View Terminal mode """
    name = 'system_view'
    pass


class CmdLineMode:
    """ CmdLine Terminal Mode """
    _name = 'cmdline'

    def __init__(self,
                 enter_command,
                 check_error_string,
                 password,
                 device):
        self._enter_command = enter_command
        self._check_error_string = check_error_string
        self._password = password
        self.device = device

    def __call__(self, *args, **kwargs):
        return self.enter()

    @property
    def _logger(self):
        return self.device._logger

    async def enter(self):
        """Entering to cmdline-mode"""
        self._logger.info("Entering to cmdline mode")

        output = await self.device.send_command(self._enter_command, pattern="\[Y\/N\]")
        output += await self.device.send_command("Y", pattern="password\:")
        output += await self.device.send_command(self._password)

        logger.debug("cmdline mode output: %s" % repr(output))

        logger.info("Checking cmdline mode")
        if self._check_error_string in output:
            raise ValueError("Failed to enter to cmdline mode")
        self.device.current_terminal = self

        return output
