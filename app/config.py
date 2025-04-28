"""
Loads and provides access to the application configuration from `config.yaml`.
"""

import yaml
from pathlib import Path
from app.logger import logger
import os

class Config:
    """
    Singleton class for loading and accessing configuration settings.
    """
    _config: dict = None
    _default: dict = None

    @classmethod
    def load_config(cls, config_path: Path):
        """
        Load the configuration from the specified YAML file.
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as file:
            cls._config = yaml.safe_load(file)

        if cls._config is None:
            raise ValueError("Configuration file is empty or invalid.")

        logger.info("Configuration loaded successfully.")

    @classmethod
    def load_default(cls):
        """
        Load the default configuration from resources.
        """
        default_config_path = Path("resources/config.default.yaml")
        with default_config_path.open("r", encoding="utf-8") as file:
            cls._default = yaml.safe_load(file)

        dcs_mission_dir = os.path.expanduser("~\\Saved Games\\DCS.release_server\\Missions") 
        cls._default["server"]["dcs_mission_dir"] = dcs_mission_dir
        

    @classmethod
    def get(cls, key: str):
        """
        Retrieve a specific configuration value by key.
        Supports nested keys using dot notation (e.g., "server.dcs_saved_game_dir").

        When a key is not found, it will return the default value from the default config.
        """

        keys = key.split(".")
        config = cls._config or {}
        default_config = cls._default or {}

        for k in keys:
            if k in config:
                config = config[k]
            elif k in default_config:
                config = default_config[k]
            else:
                raise KeyError(f"Key '{key}' not found in configuration.")
            default_config = default_config.get(k, {})

        return config
    
    @classmethod
    def get_user_home_dir(cls) -> str:
        """
        Get the default Windows user home directory.
        Returns:
            str: The path to the user's home directory.
        """
        import os
        return os.path.expanduser("~")


# Load the configuration at startup
Config.load_default()
try:
    Config.load_config(Path("config.yaml"))
except (FileNotFoundError, ValueError, KeyError) as e:
    logger.error(f"Error loading config.yaml: {e}")
    input("Press Enter to exit...")
    exit(1)
