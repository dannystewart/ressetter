"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

from __future__ import annotations

import argparse
import sys

from dsbase import ArgParser, LocalLogger

from ressetter import DisplaySettings, ResSetter
from ressetter.config import config

logger = LocalLogger().get_logger()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments, using config values as defaults."""
    parser = argparse.ArgumentParser(description="Set display resolution and refresh rate.")
    parser.add_argument(
        "--width",
        type=int,
        default=config.display["width"],
        help=f"width of the display resolution (default: {config.display['width']})",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=config.display["height"],
        help=f"weight of the display resolution (default: {config.display['height']})",
    )
    parser.add_argument(
        "--refresh",
        type=int,
        default=config.display["refresh_rate"],
        help=f"refresh rate of the display in Hz (default: {config.display['refresh_rate']})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=config.background["timeout"],
        help=f"timeout in seconds for background mode (default: {config.background['timeout']})",
    )
    parser.add_argument(
        "--set-delay",
        type=int,
        default=config.background["set_delay"],
        help=f"seconds before attempting to set display (default: {config.background['set_delay']})",
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=config.background["retry_delay"],
        help=f"seconds between retries (default: {config.background['retry_delay']})",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=config.background["max_retries"],
        help=f"maximum number of retries (default: {config.background['max_retries']})",
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
