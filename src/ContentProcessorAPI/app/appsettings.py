# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class ModelBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=False)


class AppConfiguration(ModelBaseSettings):
    app_storage_blob_url: str
    app_storage_queue_url: str
    app_cosmos_connstr: str
    app_cosmos_database: str
    app_cosmos_container_schema: str
    app_cosmos_container_process: str
    app_cps_configuration: str
    app_cps_processes: str
    app_message_queue_extract: str
    app_cps_max_filesize_mb: int
    app_logging_enable: bool
    app_logging_level: str


# Read .env file
# Get Current Path + .env file
env_file_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_file_path)

app_config: AppConfiguration | None = None


def get_app_config() -> AppConfiguration:
    global app_config
    if app_config is None:
        app_config = AppConfiguration()
        if app_config.app_logging_enable:
            logging_level = getattr(logging, app_config.app_logging_level)
            logging.basicConfig(level=logging_level)
        else:
            logging.disable(logging.CRITICAL)
    return app_config
