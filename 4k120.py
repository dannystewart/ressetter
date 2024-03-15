"""
Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz.
"""

import argparse

import win32api
import win32con

# Set default values (4K @ 120 Hz)
WIDTH = 3840
HEIGHT = 2160
REFRESH_RATE = 120


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Set display resolution and refresh rate."
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=WIDTH,
        help="Width of the display resolution (default: 3840 for 4K)",
    )
    parser.add_argument(
        "-ht",
        "--height",
        type=int,
        default=HEIGHT,
        help="Height of the display resolution (default: 2160 for 4K)",
    )
    parser.add_argument(
        "-r",
        "--refresh",
        type=int,
        default=REFRESH_RATE,
        help="Refresh rate of the display (default: 120 Hz)",
    )
    return parser.parse_args()


def already_set_correctly(devmode, width, height, refresh_rate):
    """
    Check to see if the current display settings already match the desired settings.

    Args:
        devmode (pywintypes.DEVMODEType): The current display settings.
        width (int): The width of the display resolution. Default is 3840 for 4K.
        height (int): The height of the display resolution. Default is 2160 for 4K.
        refresh_rate (int): The refresh rate to check. Default is 120 Hz.

    Returns:
        bool: True if the display settings match the desired settings, False otherwise.
    """
    if (
        devmode.PelsWidth == width
        and devmode.PelsHeight == height
        and devmode.DisplayFrequency == refresh_rate
    ):
        print(f"Display is already set to {width}x{height} at {refresh_rate} Hz.")
        return True
    return False


def set_display_settings(devmode, width, height, refresh_rate):
    """
    Set the display resolution and refresh rate for the primary display.

    Args:
        devmode (pywintypes.DEVMODEType): The current display settings.
        width (int): The width of the display resolution. Default is 3840 for 4K.
        height (int): The height of the display resolution. Default is 2160 for 4K.
        refresh_rate (int): The refresh rate to set. Default is 120 Hz.

    Returns:
        bool: True if the display settings were set successfully, False otherwise.
    """
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


def main():
    """Main function."""
    args = parse_args()
    devmode = win32api.EnumDisplaySettings(None, win32con.ENUM_CURRENT_SETTINGS)

    if not already_set_correctly(devmode, args.width, args.height, args.refresh):
        set_display_settings(devmode, args.width, args.height, args.refresh)


if __name__ == "__main__":
    main()
