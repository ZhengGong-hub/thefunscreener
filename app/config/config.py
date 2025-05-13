from pathlib import Path
import os
from dotenv import load_dotenv
from typing import Dict, Any
from pydantic import BaseModel, Field

class Paths(BaseModel):
    """Configuration for all file system paths

    Attributes:
        base_dir: Base directory for the application
        input_dir: Directory for input data
        output_dir: Directory for output data
        temp_dir: Directory for temporary files
    """

    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    # relative path
    data_output_dir: Path = Field(default_factory=lambda: Path("data_output"))

    @property
    def full_input_dir(self) -> Path:
        """Get full path to input directory."""
        return self.base_dir / self.data_output_dir


class LLMConfig(BaseModel):
    """
    This is a placeholder for the LLM config
    """
    pass


class DatabaseConfig(BaseModel):
    """Configuration for database

    Attributes:
        db_config: Database configuration dictionary
    """
    db_config: Dict[str, Any] = Field(default_factory=dict)


class Config:
    """Main configuration class that combines all configuration aspects

    This class loads and validates all configuration from environment variables
    and provides access to all configuration sections.
    """

    # Configuration sections
    paths: Paths = Field(default_factory=Paths)
    llm: LLMConfig
    database: DatabaseConfig
    api_key: str = Field(default="")

    @classmethod
    def load_configuration(cls) -> "type[Config]":
        """Load and validate all configuration from environment variables.

        Returns:
            Config: A validated configuration instance
        """
        # Load environment variables
        # define which .env file to be used
        env_file = ".env"
        env_file_encoding = "utf-8"  # default encoding
        load_dotenv(dotenv_path=env_file, override=True, encoding=env_file_encoding)

        # Configure postgres database
        db_config = {
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
        }

        # Create config instance
        cls.llm = LLMConfig()
        cls.database = DatabaseConfig(db_config=db_config)
        cls.paths = Paths()
        cls.api_key = os.getenv("API_KEY", "")
        return cls
