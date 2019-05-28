"""
Juniper Terminal Modes
"""
from aionet.vendors.terminal_modes.base import BaseTerminalMode
from aionet.vendors.terminal_modes.cisco import ConfigMode as CiscoConfigMode


class ConfigMode(CiscoConfigMode):
    pass


class CliMode(BaseTerminalMode):
    name = 'cli_mode'

    def exit(self):
        pass
