import threading
import time
from typing import Any

from pynput import keyboard, mouse

from display_settings import DisplaySettings


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
            activity_timer = threading.Timer(
                self.delay_before_set, self.display_settings.set_display_settings
            )
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
