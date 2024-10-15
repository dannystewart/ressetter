"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

import argparse
import atexit
import ctypes
import os
import sys
import tempfile
import time

import psutil

from display_settings import DisplaySettings
from input_monitor import InputMonitor

# Set default values (4K @ 120 Hz)
WIDTH = 3840
HEIGHT = 2160
REFRESH_RATE = 120
INACTIVITY_TIMEOUT_MINUTES = 10


def already_running() -> bool:
    """Check if the script is already running using a file-based lock."""
    lock_file = os.path.join(tempfile.gettempdir(), "DisplaySettingsScript.lock")
    try:
        # Check if the process with the stored PID is still running
        if os.path.exists(lock_file):
            with open(lock_file) as f:
                pid = int(f.read().strip())
            if psutil.pid_exists(pid):
                return True  # Process is still running

        # Create new lock file with our PID
        with open(lock_file, "w") as f:
            f.write(str(os.getpid()))

        # Register function to remove lock file on script exit
        atexit.register(lambda: os.remove(lock_file) if os.path.exists(lock_file) else None)
        return False
    except Exception as e:
        print(f"Error checking/creating lock file: {e}")
        return False


def show_message_box(message: str, title: str) -> None:
    """Display a Windows message box with the given message and title."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    timeout_desc = f"Inactivity timeout in minutes (default: {INACTIVITY_TIMEOUT_MINUTES})"

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
    parser.add_argument(
        "-b",
        "--background",
        action="store_true",
        help="Run in background mode, monitoring for inactivity",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=INACTIVITY_TIMEOUT_MINUTES,
        help=timeout_desc,
    )
    return parser.parse_args()


def run_background_mode(display: DisplaySettings, timeout: int) -> None:
    """Run the script in background mode, monitoring for inactivity to set display settings."""
    monitor = InputMonitor(display, timeout)
    try:
        monitor.start()
        print(
            "Running in background mode. Monitoring input. "
            f"Will set display settings after {timeout} minutes of inactivity."
        )
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping input monitoring.")
    finally:
        monitor.stop()


def main() -> None:
    """
    Parse command-line arguments and instantiate DisplaySettings. Check to see if the current
    display settings match the desired settings. If not, set them.
    """
    args = parse_args()

    if args.background and already_running():
        show_message_box("An instance of this script is already running.", "4K120")
        sys.exit(0)

    display = DisplaySettings(args.width, args.height, args.refresh)

    if args.background:
        run_background_mode(display, args.timeout)
    elif not display.already_set_correctly():
        display.set_display_settings()


if __name__ == "__main__":
    main()
