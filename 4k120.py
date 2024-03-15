"""
Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz.
"""

import win32api
import win32con

# Values for 4K @ 120 Hz
WIDTH = 3840
HEIGHT = 2160
REFRESH_RATE = 120


def set_display(width=WIDTH, height=HEIGHT, refresh_rate=REFRESH_RATE):
    """
    Set the display resolution and refresh rate for the primary display.

    Args:
        width (int): The width of the display resolution. Default is 3840 for 4K.
        height (int): The height of the display resolution. Default is 2160 for 4K.
        refresh_rate (int): The refresh rate to set. Default is 120 Hz.

    Returns:
        bool: True if the display settings were set successfully, False otherwise.
    """
    devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)

    if (  # Check if the current settings already match the desired settings
        devmode.PelsWidth == width
        and devmode.PelsHeight == height
        and devmode.DisplayFrequency == refresh_rate
    ):
        print(f"Display is already set to {width}x{height} and {refresh_rate} Hz.")
        return True

    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.DisplayFrequency = refresh_rate

    try:
        change_result = win32api.ChangeDisplaySettings(devmode, 0)
        if change_result == win32con.DISP_CHANGE_SUCCESSFUL:
            print(
                f"Display set to {width}x{height} and {refresh_rate} Hz successfully."
            )
            return True
        print(f"Changing display settings failed with result {change_result}.")
        return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False


if __name__ == "__main__":
    set_display()
