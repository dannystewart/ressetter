"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

import argparse

from display_settings import DisplaySettings

# Set default values (4K @ 120 Hz)
WIDTH = 3840
HEIGHT = 2160
REFRESH_RATE = 120


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Set display resolution and refresh rate.")
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


def main():
    """
    Parse command-line arguments and instantiate DisplaySettings. Check to see if the
    current display settings match the desired settings. If not, set them.
    """
    args = parse_args()
    display = DisplaySettings(args.width, args.height, args.refresh)

    if not display.already_set_correctly():
        display.set_display_settings()


if __name__ == "__main__":
    main()
