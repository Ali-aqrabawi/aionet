from aionet.vendors.terminal_modes.juniper import CliMode,ConfigMode
from aionet.vendors.devices.base_junos import BAseJunOSDevice


class JuniperJunOS(BAseJunOSDevice):
    """Class for working with Juniper JunOS"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cli_mode = CliMode(
            enter_command=type(self)._cli_command,
            check_string=type(self)._cli_check,
            exit_command='',
            device=self
        )

        self.config_mode = ConfigMode(
            enter_command=type(self)._config_command,
            check_string=type(self)._config_check,
            exit_command='exit',
            device=self,
            parent=self.cli_mode

        )

    _cli_check = ">"
    """Checking string for shell mode"""

    _cli_command = "cli"
    """Command for entering to cli mode"""

    _config_check = "#"
    """Checking string for shell mode"""

    _config_command = "configure"
    """Command for entering to cli mode"""

    async def _session_preparation(self):
        await super()._session_preparation()
        await self.cli_mode()

