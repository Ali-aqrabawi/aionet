"""Subclass specific to Aruba AOS 8.x"""

import re

from aionet.vendors.devices.base_ios import BaseIOSDevice


class ArubaAOS8(BaseIOSDevice):
    """Class for working with Aruba OS 8.X"""

    _disable_paging_command = "no paging"
    """Command for disabling paging"""

    _config_exit = "end"
    """Command for existing from configuration mode to privilege exec"""

    _config_check = "] (config"
    """Checking string in prompt. If it's exist im prompt - we are in configuration mode"""

    _pattern = r"\({prompt}.*?\) [*^]?\[.*?\] (\(.*?\))?\s?[{delimiters}]"
    """Pattern for using in reading buffer. When it found processing ends"""

    async def _set_base_prompt(self):
        """
        Setting two important vars:

            base_prompt - textual prompt in CLI (usually hostname)
            base_pattern - regexp for finding the end of command. It's platform specific parameter

        For Aruba AOS 8 devices base_pattern is "(prompt) [node] (\(.*?\))?\s?[#|>]
        """
        self._logger.info("Host {}: Setting base prompt".format(self.host))
        prompt = await self._find_prompt()
        prompt = prompt.split(")")[0]
        # Strip off trailing terminator
        self._base_prompt = prompt[1:]
        delimiters = map(re.escape, type(self)._delimiter_list)
        delimiters = r"|".join(delimiters)
        base_prompt = re.escape(self._base_prompt[:12])
        pattern = type(self)._pattern
        self._base_pattern = pattern.format(prompt=base_prompt, delimiters=delimiters)
        self._logger.debug("Base Prompt: %s" % self._base_prompt)
        self._logger.debug("Base Pattern: %s" % self._base_pattern)
        return self._base_prompt
