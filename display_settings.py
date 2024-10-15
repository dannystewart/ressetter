import win32api  # type: ignore
import win32con  # type: ignore


class DisplaySettings:
    """
    Class to store and manage display settings.

    Attributes:
        width: The width of the display resolution. Default is 3840 for 4K.
        height: The height of the display resolution. Default is 2160 for 4K.
        refresh_rate: The refresh rate to check. Default is 120 Hz.
        devmode: The current display settings.
    """

    def __init__(self, width: int, height: int, refresh_rate: int):
        self.width = width
        self.height = height
        self.refresh_rate = refresh_rate
        self.devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)

    def already_set_correctly(self) -> bool:
        """
        Check to see if the current display settings already match the desired settings. Returns
        True if the display settings match the desired settings, False otherwise.
        """
        if (
            self.devmode.PelsWidth == self.width
            and self.devmode.PelsHeight == self.height
            and self.devmode.DisplayFrequency == self.refresh_rate
        ):
            print(
                f"Display is already set to {self.width}x{self.height} at {self.refresh_rate} Hz."
            )
            return True
        return False

    def set_display_settings(self) -> bool:
        """
        Set the display resolution and refresh rate for the primary display. Returns True if the
        display settings were set successfully, False otherwise.
        """
        self.devmode.PelsWidth = self.width
        self.devmode.PelsHeight = self.height
        self.devmode.DisplayFrequency = self.refresh_rate

        try:
            change_result = win32api.ChangeDisplaySettings(self.devmode, 0)
            if change_result == win32con.DISP_CHANGE_SUCCESSFUL:
                print(
                    f"Display set to {self.width}x{self.height} and {self.refresh_rate} Hz successfully."
                )
                return True
            print(f"Changing display settings failed with result {change_result}.")
            return False
        except Exception as e:
            print(f"Exception occurred: {e}")
            return False
