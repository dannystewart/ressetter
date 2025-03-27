"""Configuration management for ResSetter."""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

import toml

from dsbase import EnvManager, LocalLogger, PathKeeper


class Config:
    """Configuration manager for ResSetter."""

    # Default configuration values
    DEFAULT_CONFIG: ClassVar[dict[str, Any]] = {
        "display": {
            "width": 3840,
            "height": 2160,
            "refresh_rate": 120,
        },
        "background": {
            "timeout": 300,
            "set_delay": 5,
            "retry_delay": 10,
            "max_retries": 3,
        },
    }

    def __init__(self) -> None:
        """Initialize the config manager."""
        self.logger = LocalLogger().get_logger()
        self.paths = PathKeeper("ressetter")
        self.env = EnvManager()
        self.env.add_var("RESSETTER_CONFIG", description="Path to the configuration file")
        self.config_data = self.DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from TOML file."""
        config_paths = [
            # Current directory
            Path("config.toml"),
            # User's home directory
            self.paths.from_config("config.toml"),
        ]

        # Add config path from environment variable if set
        if config_env := self.env.ressetter_config:
            config_paths.insert(0, Path(config_env))

        for config_path in config_paths:
            if config_path.exists():
                try:
                    loaded_config = toml.load(config_path)
                    self.logger.info("Loaded configuration from %s", config_path)
                    self._update_config(loaded_config)
                    return
                except Exception as e:
                    self.logger.error("Error loading config from %s: %s", config_path, str(e))

        self.logger.info("No configuration file found. Using default values.")

    def _update_config(self, loaded_config: dict[str, Any]) -> None:
        """Update configuration with loaded values."""
        # Update display settings if present
        if display_config := loaded_config.get("display"):
            self.config_data["display"].update(display_config)

        # Update background settings if present
        if background_config := loaded_config.get("background"):
            self.config_data["background"].update(background_config)

    @property
    def display(self) -> dict[str, int]:
        """Get display settings."""
        return self.config_data["display"]

    @property
    def background(self) -> dict[str, int]:
        """Get background mode settings."""
        return self.config_data["background"]


# Singleton instance
config = Config()
