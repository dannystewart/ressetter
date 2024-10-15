import threading
import time
from typing import Any

from pynput import keyboard, mouse

from display_settings import DisplaySettings


class InputMonitor:
    """Monitor for keyboard and mouse input to set display settings after a period of inactivity."""

    def __init__(self, display_settings: DisplaySettings, timeout_minutes: int, max_retries: int, retry_delay: int):
        self.display_settings = display_settings
        self.timeout_seconds = timeout_minutes * 60
        self.delay_before_set = 5  # Delay before setting after inactivity (seconds)
        self.last_activity_time = time.time()
        self.timer: threading.Timer | None = None
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)
        self.max_retries = max_retries
        self.retry_delay = retry_delay

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
            self.attempt_display_settings_change()
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

    def attempt_display_settings_change(self) -> None:
        """Attempt to change display settings with retries."""
        for attempt in range(self.max_retries):
            if self.display_settings.already_set_correctly():
                print("Display settings are already correct.")
                return

            if self.display_settings.set_display_settings():
                print(f"Display settings changed successfully on attempt {attempt + 1}.")
                return

            if attempt < self.max_retries - 1:
                print(f"Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)

        print(f"Failed to change display settings after {self.max_retries} attempts.")
