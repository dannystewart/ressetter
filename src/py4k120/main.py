"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

from __future__ import annotations

import argparse
import atexit
import ctypes
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import psutil
import toml

from py4k120 import DisplaySettings, InputMonitor

DEFAULT_CONFIG: dict[str, dict[str, int]] = {
    "display": {
        "width": 3840,
        "height": 2160,
        "refresh_rate": 120,
    },
    "input": {
        "timeout": 300,
        "delay_before_set": 5,
        "delay_before_retry": 10,
        "max_retries": 3,
    },
}


def create_default_config(config_file: Path) -> None:
    """Create a default configuration file."""
    try:
        with config_file.open("w") as f:
            toml.dump(DEFAULT_CONFIG, f)
    except Exception as e:
        print(f"Error creating default config file: {e}")


def load_config(config_file: str = "config.toml") -> dict[str, Any]:
    """Load configuration from TOML file. Create default file if it doesn't exist."""
    config_path = Path(config_file)

    if not config_path.exists():
        create_default_config(config_path)
        print(f"Created default config file: {config_file}")

    try:
        with config_path.open() as f:
            config = toml.load(f)

        # Ensure all expected keys are present
        for section, values in DEFAULT_CONFIG.items():
            if section not in config:
                config[section] = {}
            for key, value in values.items():
                if key not in config[section]:
                    config[section][key] = value
                    print(f"Added missing config value: {section}.{key} = {value}")

        # If any values were added, update the file
        if config != DEFAULT_CONFIG:
            with config_path.open("w") as f:
                toml.dump(config, f)

        return config
    except Exception as e:
        print(f"Error reading config file: {e}")
        print("Using default configuration.")
        return DEFAULT_CONFIG


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
        print(f"Error checking/creating lock file: {e}")
        return False


def show_message_box(message: str, title: str) -> None:
    """Display a Windows message box with the given message and title."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)  # type: ignore


def parse_args(config: dict[str, Any]) -> argparse.Namespace:
    """Parse command-line arguments, using config values as defaults."""
    parser = argparse.ArgumentParser(description="Set display resolution and refresh rate.")
    parser.add_argument(
        "--width",
        type=int,
        default=config["display"]["width"],
        help="Width of the display resolution (default: 3840 for 4K)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=config["display"]["height"],
        help="Height of the display resolution (default: 2160 for 4K)",
    )
    parser.add_argument(
        "--refresh",
        type=int,
        default=config["display"]["refresh_rate"],
        help="Refresh rate of the display (default: 120 Hz)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=config["input"]["timeout"],
        help="Timeout in seconds for background mode (default: 300)",
    )
    parser.add_argument(
        "--set-delay",
        type=int,
        default=config["input"]["delay_before_set"],
        help="Seconds before attempting to set display settings",
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=config["input"]["delay_before_retry"],
        help="Seconds between retries",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=config["input"]["max_retries"],
        help="Maximum number of retries",
    )
    parser.add_argument("--background", action="store_true", help="Run in background mode")
    return parser.parse_args()


def run_background_mode(
    display: DisplaySettings, timeout: int, set_delay: int, retry_delay: int, max_retries: int
) -> None:
    """Run the script in background mode, monitoring for inactivity to set display settings."""
    monitor = InputMonitor(display, timeout, set_delay, retry_delay, max_retries)
    try:
        monitor.start()
        timeout_minutes = timeout // 60  # Convert seconds to minutes for display
        print(
            "Running in background mode, monitoring input. "
            f"Will set display settings after {timeout_minutes} minute{'s' if timeout_minutes != 1 else ''} of inactivity."
        )
        print(
            f"Delay before set after inactivity: {set_delay} second{'s' if set_delay != 1 else ''}, "
            f"delay before retrying: {retry_delay} second{'s' if retry_delay != 1 else ''}, "
            f"max retries: {max_retries}"
        )
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping input monitoring.")
    finally:
        monitor.stop()


def main() -> None:
    """Set the display settings if needed, or run in background mode."""
    config = load_config()
    args = parse_args(config)

    if args.background and already_running():
        show_message_box("An instance of this script is already running.", "4K120")
        sys.exit(0)

    display = DisplaySettings(args.width, args.height, args.refresh)

    if args.background:
        run_background_mode(
            display, args.timeout, args.set_delay, args.retry_delay, args.max_retries
        )
    elif not display.already_set_correctly():
        display.set_display_settings()


if __name__ == "__main__":
    main()
