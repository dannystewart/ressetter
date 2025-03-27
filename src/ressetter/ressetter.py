"""Script to set the display resolution and refresh rate for the primary display to 4K @ 120 Hz."""

from __future__ import annotations

import atexit
import ctypes
import os
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import psutil

from dsbase import LocalLogger

from ressetter import DisplaySettings, InputMonitor

if TYPE_CHECKING:
    from logging import Logger


@dataclass
class ResSetter:
    """Main class for the ResSetter script."""

    display: DisplaySettings
    timeout: int
    set_delay: int
    retry_delay: int
    max_retries: int

    logger: Logger = field(init=False)

    def __post_init__(self) -> None:
        self.logger = LocalLogger().get_logger()
        self.monitor = InputMonitor(
            self.display, self.timeout, self.set_delay, self.retry_delay, self.max_retries
        )

    def run_background(self) -> None:
        """Run the script in background mode, monitoring for inactivity to set display settings."""
        try:
            self.monitor.start()
            timeout_minutes = self.timeout // 60  # Convert seconds to minutes for display
            self.logger.info("Running in background mode, monitoring input.")
            self.logger.info(
                "Will set display settings after %d minutes of inactivity.", timeout_minutes
            )
            self.logger.debug(
                "Delay before set after inactivity: %d %s, delay before retrying: %d %s, max retries: %d",
                self.set_delay,
                "second" if self.set_delay == 1 else "seconds",
                self.retry_delay,
                "second" if self.retry_delay == 1 else "seconds",
                self.max_retries,
            )
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping input monitoring.")
        finally:
            self.monitor.stop()

    @property
    def already_running(self) -> bool:
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
            self.logger.error("Error checking/creating lock file: %s", str(e))
            return False

    @staticmethod
    def show_message_box(message: str, title: str) -> None:
        """Display a Windows message box with the given message and title."""
        ctypes.windll.user32.MessageBoxW(0, message, title, 0)  # type: ignore
