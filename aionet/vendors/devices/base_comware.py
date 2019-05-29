"""
ComwareLikeDevice Class is abstract class for using in HP Comware like devices

Connection Method are based upon AsyncSSH and should be running in asyncio loop
"""

import re

from aionet.vendors.terminal_modes.hp import SystemView
from aionet.vendors.devices.base import BaseDevice


class BaseComwareDevice(BaseDevice):
    """
    This Class for working with hp comware like devices

    HP Comware like devices having several concepts:

    * user exec or user view. This mode is using for getting information from device
    * system view. This mode is using for configuration system
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_terminal = None  # State Machine for the current Terminal mode of the session
        self.system_view = SystemView(
            enter_command=type(self)._system_view_enter,
            exit_command=type(self)._system_view_exit,
            check_string=type(self)._system_view_check,
            device=self
        )

    _delimiter_list = [">", "]"]
    """All this characters will stop reading from buffer. It mean the end of device prompt"""

    _delimiter_left_list = ["<", "["]
    """Begging prompt characters. Prompt must contain it"""

    _pattern = r"[{delimiter_left}]{prompt}[\-\w]*[{delimiter_right}]"
    """Pattern for using in reading buffer. When it found processing ends"""

    _disable_paging_command = "screen-length disable"
    """Command for disabling paging"""

    _system_view_enter = "system-view"
    """Command for entering to system view"""

    _system_view_exit = "return"
    """Command for existing from system view to user view"""

    _system_view_check = "]"
    """Checking string in prompt. If it's exist im prompt - we are in system view"""

    async def _session_preparation(self):
        """ Prepare Session """
        await super()._session_preparation()
        await self._disable_paging()

    async def _set_base_prompt(self):
        """
        Setting two important vars
            base_prompt - textual prompt in CLI (usually hostname)
            base_pattern - regexp for finding the end of command. IT's platform specific parameter

        For Comware devices base_pattern is "[\]|>]prompt(\-\w+)?[\]|>]
        """
        self._logger.info("Setting base prompt")
        prompt = await self._find_prompt()
        # Strip off trailing terminator
        self._base_prompt = prompt[1:-1]
        delimiter_right = map(re.escape, type(self)._delimiter_list)
        delimiter_right = r"|".join(delimiter_right)
        delimiter_left = map(re.escape, type(self)._delimiter_left_list)
        delimiter_left = r"|".join(delimiter_left)
        base_prompt = re.escape(self._base_prompt[:12])
        pattern = type(self)._pattern
        self._base_pattern = pattern.format(
            delimiter_left=delimiter_left,
            prompt=base_prompt,
            delimiter_right=delimiter_right,
        )
        self._logger.debug("Base Prompt: %s" % self._base_prompt)
        self._logger.debug("Base Pattern: %s" % self._base_pattern)
        return self._base_prompt

    async def send_config_set(self, config_commands=None, exit_system_view=False):
        """
        Sending configuration commands to device
        Automatically exits/enters system-view.

        :param list config_commands: iterable string list with commands for applying to network devices in system view
        :param bool exit_system_view: If true it will quit from system view automatically
        :return: The output of this commands
        """

        if config_commands is None:
            return ""

        # Send config commands
        output = await self.system_view()
        output += await super().send_config_set(config_commands=config_commands)

        if exit_system_view:
            output += await self.system_view.exit()

        output = self._normalize_linefeeds(output)
        self._logger.debug("Config commands output: %s" % repr(output))
        return output
