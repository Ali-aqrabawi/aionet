"""Subclass specific to Fujitsu Blade Switch"""

import re

from aionet.vendors.devices.base_ios import BaseIOSDevice


class FujitsuSwitch(BaseIOSDevice):
    """Class for working with Fujitsu Blade switch"""

    _pattern = r"\({prompt}.*?\) (\(.*?\))?[{delimiters}]"
    """Pattern for using in reading buffer. When it found processing ends"""

    _disable_paging_command = "no pager"
    """Command for disabling paging"""

    _config_enter = "conf"
    """Command for entering to configuration mode"""

    async def _set_base_prompt(self):
        """
        Setting two important vars
            base_prompt - textual prompt in CLI (usually hostname)
            base_pattern - regexp for finding the end of command. IT's platform specific parameter

        For Fujitsu devices base_pattern is "(prompt) (\(.*?\))?[>|#]"
        """
        self._logger.info("Setting base prompt")
        prompt = await self._find_prompt()
        # Strip off trailing terminator
        self._base_prompt = prompt[1:-3]
        delimiters = map(re.escape, type(self)._delimiter_list)
        delimiters = r"|".join(delimiters)
        base_prompt = re.escape(self._base_prompt[:12])
        pattern = type(self)._pattern
        self._base_pattern = pattern.format(prompt=base_prompt, delimiters=delimiters)
        self._logger.debug("Base Prompt: %s" % self._base_prompt)
        self._logger.debug("Base Pattern: %s" % self._base_pattern)
        return self._base_prompt

    @staticmethod
    def _normalize_linefeeds(a_string):
        """
        Convert '\r\r\n','\r\n', '\n\r' to '\n and remove extra '\n\n' in the text
        """
        newline = re.compile(r"(\r\r\n|\r\n|\n\r)")
        return newline.sub("\n", a_string).replace("\n\n", "\n")
