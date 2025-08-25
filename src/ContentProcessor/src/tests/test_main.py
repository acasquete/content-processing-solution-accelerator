import os
import os
import pytest
from main import Application


class DummyHandler:
    def __init__(self, appContext, step_name):
        self.handler_name = step_name
        self.appContext = appContext
        self.step_name = step_name
        self.exitcode = None

    def connect_queue(self, *args):
        print(f"Connecting queue for handler: {self.handler_name}")


@pytest.mark.asyncio
async def test_application_run(mocker):
    # Mock the application context and configuration
    mock_app_context = mocker.MagicMock()
    mock_app_context.configuration.app_process_steps = ["extract", "transform"]

    # Mock the handler loader to return a DummyHandler
    mocker.patch(
        "libs.process_host.handler_type_loader.load",
        side_effect=lambda name: DummyHandler,
    )

    # Mock the HandlerHostManager instance
    mocker.patch(
        "libs.process_host.handler_process_host.HandlerHostManager"
    ).return_value

    # Set up environment variables required by the application
    env = {
        "APP_STORAGE_QUEUE_URL": "https://example.com/queue",
        "APP_STORAGE_BLOB_URL": "https://example.com/blob",
        "APP_PROCESS_STEPS": "extract,map",
        "APP_MESSAGE_QUEUE_INTERVAL": "2",
        "APP_MESSAGE_QUEUE_VISIBILITY_TIMEOUT": "1",
        "APP_MESSAGE_QUEUE_PROCESS_TIMEOUT": "2",
        "APP_LOGGING_ENABLE": "True",
        "APP_LOGGING_LEVEL": "DEBUG",
        "APP_CPS_PROCESSES": "4",
        "APP_CPS_CONFIGURATION": "value",
        "APP_CONTENT_UNDERSTANDING_ENDPOINT": "https://example.com/content",
        "APP_AZURE_OPENAI_ENDPOINT": "https://example.com/openai",
        "APP_AZURE_OPENAI_MODEL": "model-name",
        "APP_COSMOS_CONNSTR": "AccountEndpoint=https://example.com;AccountKey=key;",
        "APP_COSMOS_DATABASE": "database-name",
        "APP_COSMOS_CONTAINER_PROCESS": "container-process",
        "APP_COSMOS_CONTAINER_SCHEMA": "container-schema",
    }
    mocker.patch.dict(os.environ, env, clear=True)

    # Initialize the application with the mocked context
    mocker.patch.object(
        Application, "_initialize_application", return_value=mock_app_context
    )
    app = Application()

    # Run the application
    await app.run(test_mode=True)
