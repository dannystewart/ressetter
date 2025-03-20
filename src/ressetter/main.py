"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

from __future__ import annotations

import argparse
import sys

from dsbase.log import LocalLogger
from dsbase.util import ArgParser

from ressetter import DisplaySettings, ResSetter

logger = LocalLogger().get_logger()

# Default display settings
DEFAULT_WIDTH = 3840
DEFAULT_HEIGHT = 2160
DEFAULT_REFRESH = 120

# Default background mode settings
DEFAULT_TIMEOUT = 300
DEFAULT_SET_DELAY = 5
DEFAULT_RETRY_DELAY = 10
DEFAULT_MAX_RETRIES = 3


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments, using config values as defaults."""
    parser = argparse.ArgumentParser(description="Set display resolution and refresh rate.")
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help=f"width of the display resolution (default: {DEFAULT_WIDTH})",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=DEFAULT_HEIGHT,
        help=f"weight of the display resolution (default: {DEFAULT_HEIGHT})",
    )
    parser.add_argument(
        "--refresh",
        type=int,
        default=DEFAULT_REFRESH,
        help=f"refresh rate of the display in Hz (default: {DEFAULT_REFRESH})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"timeout in seconds for background mode (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "--set-delay",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"seconds before attempting to set display (default: {DEFAULT_SET_DELAY})",
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=DEFAULT_RETRY_DELAY,
        help=f"seconds between retries (default: {DEFAULT_RETRY_DELAY})",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f"maximum number of retries (default: {DEFAULT_MAX_RETRIES})",
    )
    parser.add_argument("--background", action="store_true", help="run in background mode")
    return parser.parse_args()


def main() -> None:
    """Set the display settings if needed, or run in background mode."""
    parser = ArgParser(description=__doc__, arg_width=24, max_width=120)
    args = parser.parse_args()

    display = DisplaySettings(args.width, args.height, args.refresh)
    ressetter = ResSetter(display, args.timeout, args.set_delay, args.retry_delay, args.max_retries)

    if args.background and ressetter.already_running:
        ressetter.show_message_box("An instance of this script is already running.", "4K120")
        sys.exit(0)

    if args.background:
        ressetter.run_background()
    elif not display.already_set_correctly:
        display.set_display_settings()


if __name__ == "__main__":
    main()
