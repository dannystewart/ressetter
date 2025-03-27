from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import win32api  # type: ignore
import win32con  # type: ignore

from dsbase import LocalLogger

if TYPE_CHECKING:
    from logging import Logger

    import win32typing  # type: ignore


@dataclass
class DisplaySettings:
    """Class to store and manage display settings."""

    width: int = 3840
    height: int = 2160
    refresh_rate: int = 120
    devmode: win32typing.PyDEVMODEW = field(init=False)
    logger: Logger = field(init=False)

    def __post_init__(self):
        self.devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)
        self.logger = LocalLogger().get_logger()

    def set_display_settings(self) -> bool:
        """Set the display resolution and refresh rate for the primary display.

        Returns:
            True if the display settings were set successfully, False otherwise.
        """
        self.devmode.PelsWidth = self.width
        self.devmode.PelsHeight = self.height
        self.devmode.DisplayFrequency = self.refresh_rate

        try:
            change_result = win32api.ChangeDisplaySettings(self.devmode, 0)
            if change_result == win32con.DISP_CHANGE_SUCCESSFUL:
                self.logger.info(
                    "Display set to %sx%s and %s Hz successfully.",
                    self.width,
                    self.height,
                    self.refresh_rate,
                )
                return True
            self.logger.error("Changing display settings failed with result %s.", change_result)
            return False
        except Exception as e:
            self.logger.exception("Exception occurred: %s", str(e))
            return False

    @property
    def already_set_correctly(self) -> bool:
        """Check to see if the current display settings already match the desired settings.

        Returns:
            True if the display settings match the desired settings, False otherwise.
        """
        if (
            self.devmode.PelsWidth == self.width
            and self.devmode.PelsHeight == self.height
            and self.devmode.DisplayFrequency == self.refresh_rate
        ):
            self.logger.info(
                "Display is already set to %sx%s at %s Hz.",
                self.width,
                self.height,
                self.refresh_rate,
            )
            return True
        return False
