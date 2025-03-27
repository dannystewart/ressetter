from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pynput import keyboard, mouse

from dsbase import LocalLogger

if TYPE_CHECKING:
    from logging import Logger

    from ressetter.display_settings import DisplaySettings


@dataclass
class InputMonitor:
    """Monitor for keyboard and mouse input to set display settings after a period of inactivity."""

    display_settings: DisplaySettings
    timeout: int  # Timeout in seconds
    set_delay: int  # Delay before setting display settings in seconds
    retry_delay: int  # Delay between retries in seconds
    max_retries: int  # Maximum number of retries to set display settings

    keyboard_listener: keyboard.Listener = field(init=False)
    mouse_listener: mouse.Listener = field(init=False)

    timer: threading.Timer | None = None
    last_activity_time: float = field(default_factory=time.time)

    logger: Logger = field(init=False)

    def __post_init__(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)
        self.logger = LocalLogger().get_logger()

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
        if current_time - self.last_activity_time >= self.timeout:
            threading.Timer(self.set_delay, self.attempt_display_settings_change).start()
        self.last_activity_time = current_time
        self.reset_timer()

    def reset_timer(self) -> None:
        """Reset the inactivity timer."""
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.timeout, self.on_inactivity)
        self.timer.start()

    def on_inactivity(self) -> None:
        """Print a message when inactivity is detected."""
        self.logger.debug("Inactivity detected. Waiting for next input to set display settings.")

    def attempt_display_settings_change(self) -> None:
        """Attempt to change display settings with retries."""
        for attempt in range(self.max_retries):
            if self.display_settings.already_set_correctly:
                self.logger.info("Display settings are already correct.")
                return

            if self.display_settings.set_display_settings():
                self.logger.info(
                    "Display settings changed successfully on attempt %s.", attempt + 1
                )
                return

            if attempt < self.max_retries - 1:
                self.logger.warning(
                    "Failed to change display settings. Retrying in %s seconds.", self.retry_delay
                )
                time.sleep(self.retry_delay)

        self.logger.error("Failed to change display settings after %s attempts.", self.max_retries)
