"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

import argparse
import atexit
import ctypes
import os
import sys
import tempfile
import threading
import time
from typing import Any

import psutil
import win32api  # type: ignore
import win32con  # type: ignore
from pynput import keyboard, mouse

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


class InputMonitor:
    """Monitor for keyboard and mouse input to set display settings after a period of inactivity."""

    def __init__(self, display_settings: DisplaySettings, timeout_minutes: int):
        self.display_settings = display_settings
        self.timeout_seconds = timeout_minutes * 60
        self.delay_before_set = 5  # Delay before setting after inactivity (seconds)
        self.last_activity_time = time.time()
        self.timer: threading.Timer | None = None
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)

    def start(self) -> None:
        """Start monitoring for keyboard and mouse input."""
        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.reset_timer()

    def stop(self) -> None:
        """Stop monitoring for keyboard and mouse input."""
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        if self.timer:
            self.timer.cancel()

    def on_activity(self, *args: Any) -> None:  # noqa: ARG002
        """Reset the inactivity timer when keyboard or mouse activity is detected."""
        current_time = time.time()
        if current_time - self.last_activity_time >= self.timeout_seconds:
            activity_timer = threading.Timer(self.delay_before_set, self.display_settings.set_display_settings)
            activity_timer.start()
        self.last_activity_time = current_time
        self.reset_timer()

    def reset_timer(self) -> None:
        """Reset the inactivity timer."""
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.timeout_seconds, self.on_inactivity)
        self.timer.start()

    def on_inactivity(self) -> None:
        """Print a message when inactivity is detected."""
        print("Inactivity detected. Waiting for next input to set display settings.")


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
