"""
Juniper Terminal Modes
"""
from aionet.vendors.terminal_modes.base import BaseTerminalMode
from aionet.vendors.terminal_modes.cisco import ConfigMode as CiscoConfigMode


class ConfigMode(CiscoConfigMode):
    async def check(self, force=False):
        """Check if are in configuration mode. Return boolean"""
        if self.device.current_terminal is not None and not force:
            if self.device.current_terminal == self:
                return True
        await self.device.send_new_line()
        output = await self.device.send_new_line()

        return self._check_string in output
    pass


class CliMode(BaseTerminalMode):
    name = 'cli_mode'

    def exit(self):
        pass
