"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

from __future__ import annotations

import atexit
import ctypes
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import psutil

from dsutil import LocalLogger
from dsutil.argparser import ArgInfo, ArgParser, ArgumentsBase

from py4k120 import DisplaySettings, InputMonitor

logger = LocalLogger().get_logger()


@dataclass
class Py4K120Arguments(ArgumentsBase):
    """Class to define command-line arguments for the script."""

    # Display settings
    width: ClassVar[ArgInfo] = ArgInfo(
        "width of the display resolution (default: 3840 for 4K)", default=3840
    )
    height: ClassVar[ArgInfo] = ArgInfo(
        "height of the display resolution (default: 2160 for 4K)", default=2160
    )
    refresh: ClassVar[ArgInfo] = ArgInfo(
        "refresh rate of the display (default: 120 Hz)", default=120
    )

    # Timeout and retry values for background mode
    background: ClassVar[ArgInfo] = ArgInfo(help="run in background mode", action="store_true")
    timeout: ClassVar[ArgInfo] = ArgInfo(
        "timeout in seconds for background mode (default: 300)", default=300
    )
    set_delay: ClassVar[ArgInfo] = ArgInfo(
        "seconds before attempting to set display settings (default: 5)", default=5
    )
    retry_delay: ClassVar[ArgInfo] = ArgInfo("seconds between retries (default: 10)", default=10)
    max_retries: ClassVar[ArgInfo] = ArgInfo("maximum number of retries (default: 3)", default=3)


def show_message_box(message: str, title: str) -> None:
    """Display a Windows message box with the given message and title."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)  # type: ignore


def already_running() -> bool:
    """Check if the script is already running using a file-based lock."""
    lock_file = Path(tempfile.gettempdir()) / "DisplaySettingsScript.lock"
    try:
        # Check if the process with the stored PID is still running
        if lock_file.exists():
            with lock_file.open() as f:
                pid = int(f.read().strip())
            if psutil.pid_exists(pid):
                return True  # Process is still running

        # Create new lock file with our PID
        with lock_file.open("w") as f:
            f.write(str(os.getpid()))

        # Register function to remove lock file on script exit
        atexit.register(lambda: lock_file.unlink(missing_ok=True))
        return False
    except Exception as e:
        logger.error("Error checking/creating lock file: %s", str(e))
        return False


def run_background(
    display: DisplaySettings,
    timeout: int,
    set_delay: int,
    retry_delay: int,
    max_retries: int,
) -> None:
    """Run the script in background mode, monitoring for inactivity to set display settings."""
    monitor = InputMonitor(display, timeout, set_delay, retry_delay, max_retries)
    try:
        monitor.start()
        timeout_minutes = timeout // 60  # Convert seconds to minutes for display
        logger.info("Running in background mode, monitoring input.")
        logger.info("Will set display settings after %d minutes of inactivity.", timeout_minutes)
        logger.debug(
            "Delay before set after inactivity: %d second%s, delay before retrying: %d second%s, max retries: %d",
            set_delay,
            "" if set_delay == 1 else "s",
            retry_delay,
            "" if retry_delay == 1 else "s",
            max_retries,
        )
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping input monitoring.")
    finally:
        monitor.stop()


def main() -> None:
    """Set the display settings if needed, or run in background mode."""
    parser = ArgParser(description=__doc__, arg_width=24, max_width=120)
    parser.add_args_from_class(Py4K120Arguments)
    args = parser.parse_args()

    if args.background and already_running():
        show_message_box("An instance of this script is already running.", "4K120")
        sys.exit(0)

    display = DisplaySettings(args.width, args.height, args.refresh)

    if args.background:
        run_background(display, args.timeout, args.set_delay, args.retry_delay, args.max_retries)
    elif not display.already_set_correctly:
        display.set_display_settings()


if __name__ == "__main__":
    main()
