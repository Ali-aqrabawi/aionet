"""
JunOSLikeDevice Class is abstract class for using in Juniper JunOS like devices

Connection Method are based upon AsyncSSH and should be running in asyncio loop
"""

import re

from aionet.vendors.terminal_modes.juniper import ConfigMode
from aionet.vendors.devices.base import BaseDevice


class BAseJunOSDevice(BaseDevice):
    """
    JunOSLikeDevice Class for working with Juniper JunOS like devices

    Juniper JunOS like devices having several concepts:

    * shell mode (csh). This is csh shell for FreeBSD. This mode is not covered by this Class.
    * cli mode (specific shell). The entire configuration is usual configured in this shell:

      * operation mode. This mode is using for getting information from device
      * configuration mode. This mode is using for configuration system
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_terminal = None  # State Machine for the current Terminal mode of the session
        self.config_mode = ConfigMode(
            enter_command=type(self)._config_enter,
            exit_command=type(self)._config_check,
            check_string=type(self)._config_exit,
            device=self
        )

    _delimiter_list = ["%", ">", "#"]
    """All this characters will stop reading from buffer. It mean the end of device prompt"""

    _pattern = r"\w+(\@[\-\w]*)?[{delimiters}]"
    """Pattern for using in reading buffer. When it found processing ends"""

    _disable_paging_command = "set cli screen-length 0"
    """Command for disabling paging"""

    _config_enter = "configure"
    """Command for entering to configuration mode"""

    _config_exit = "exit configuration-mode"
    """Command for existing from configuration mode to privilege exec"""

    _config_check = "#"
    """Checking string in prompt. If it's exist im prompt - we are in configuration mode"""

    _commit_command = "commit"
    """Command for committing changes"""

    _commit_comment_command = "commit comment {}"
    """Command for committing changes with comment"""

    async def _set_base_prompt(self):
        """
        Setting two important vars
            base_prompt - textual prompt in CLI (usually username or hostname)
            base_pattern - regexp for finding the end of command. IT's platform specific parameter

        For JunOS devices base_pattern is "user(@[hostname])?[>|#]
        """
        self._logger.info("Setting base prompt")
        prompt = await self._find_prompt()
        prompt = prompt[:-1]
        # Strip off trailing terminator
        if "@" in prompt:
            prompt = prompt.split("@")[1]
        self._base_prompt = prompt
        delimiters = map(re.escape, type(self)._delimiter_list)
        delimiters = r"|".join(delimiters)
        base_prompt = re.escape(self._base_prompt[:12])
        pattern = type(self)._pattern
        self._base_pattern = pattern.format(delimiters=delimiters)
        self._logger.debug("Base Prompt: %s" % self._base_prompt)
        self._logger.debug("Base Pattern: %s" % self._base_pattern)
        return self._base_prompt

    async def send_config_set(
            self,
            config_commands=None,
            with_commit=True,
            commit_comment="",
            exit_config_mode=True,
    ):
        """
        Sending configuration commands to device
        By default automatically exits/enters configuration mode.

        :param list config_commands: iterable string list with commands for applying to network devices in system view
        :param bool with_commit: if true it commit all changes after applying all config_commands
        :param string commit_comment: message for configuration commit
        :param bool exit_config_mode: If true it will quit from configuration mode automatically
        :return: The output of these commands
        """

        if config_commands is None:
            return ""

        # Send config commands
        output = await self.config_mode()
        output += await super().send_config_set(config_commands=config_commands)
        if with_commit:
            commit = type(self)._commit_command
            if commit_comment:
                commit = type(self)._commit_comment_command.format(commit_comment)

            output += await self.send_command_expect(commit)

        if exit_config_mode:
            output += await self.config_mode.exit()

        self._logger.debug("Config commands output: %s" % repr(output))

        return output
