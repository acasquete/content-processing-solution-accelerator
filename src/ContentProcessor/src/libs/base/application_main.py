# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import inspect
import logging
import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

from libs.application.application_configuration import AppConfiguration
from libs.application.application_context import AppContext
from libs.base.application_models import AppModelBase


class AppMainBase(ABC, AppModelBase):
    application_context: AppContext = None

    @abstractmethod
    def run(self):
        raise NotImplementedError("Method run not implemented")

    def __init__(self, env_file_path: str | None = None, **data):
        super().__init__(**data)

        # Read environment variables from .env file if provided
        self._load_env(env_file_path=env_file_path)

        # Set App Context object
        self.application_context = AppContext()
        self.application_context.set_configuration(AppConfiguration())

        if self.application_context.configuration.app_logging_enable:
            # Read Configuration for Logging Level as a Text then retrive the logging level
            logging_level = getattr(
                logging, self.application_context.configuration.app_logging_level
            )
            logging.basicConfig(level=logging_level)

    def _load_env(self, env_file_path: str | None = None):
        # if .env file path is provided, load it
        # else derive the path from the derived class location
        # or Environment variable in OS will be loaded by appplication_coonfiguration.py with using pydentic_settings, BaseSettings
        if env_file_path:
            load_dotenv(dotenv_path=env_file_path)
            return env_file_path

        derived_class_location = self._get_derived_class_location()
        env_file_path = os.path.join(os.path.dirname(derived_class_location), ".env")
        load_dotenv(dotenv_path=env_file_path)
        return env_file_path

    def _get_derived_class_location(self):
        return inspect.getfile(self.__class__)
