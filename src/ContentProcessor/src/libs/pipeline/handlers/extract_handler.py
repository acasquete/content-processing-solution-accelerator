# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from libs.application.application_context import AppContext
from libs.azure_helper.content_understanding import AzureContentUnderstandingHelper
from libs.azure_helper.model.content_understanding import AnalyzedResult
from libs.pipeline.entities.pipeline_file import PipelineLogEntry
from libs.pipeline.entities.pipeline_message_context import MessageContext
from libs.pipeline.entities.pipeline_step_result import StepResult
from libs.pipeline.queue_handler_base import HandlerBase
from libs.pipeline.entities.pipeline_file import ArtifactType
from libs.pipeline.entities.schema import Schema
from libs.utils.content_understanding_schema import (
    build_content_understanding_schema,
)
from libs.utils.remote_module_loader import load_schema_from_blob
import requests


class ExtractHandler(HandlerBase):
    def __init__(self, appContext: AppContext, step_name: str, **data):
        super().__init__(appContext, step_name, **data)

    async def execute(self, context: MessageContext) -> StepResult:
        print(context.data_pipeline.get_previous_step_result(self.handler_name))

        # Resolve analyzer for the target schema.  The analyzer is created on
        # first use based on the Pydantic schema definition so that Content
        # Understanding can extract strongly typed fields without relying on the
        # generic ``prebuilt-layout`` model.
        analyzer_id = context.data_pipeline.pipeline_status.schema_id
        content_understanding_helper = AzureContentUnderstandingHelper(
            self.application_context.configuration.app_content_understanding_endpoint
        )

        try:
            # If the analyzer does not exist this call will raise an HTTPError
            content_understanding_helper.get_analyzer_detail_by_id(analyzer_id)
        except requests.exceptions.HTTPError:
            selected_schema = Schema.get_schema(
                connection_string=self.application_context.configuration.app_cosmos_connstr,
                database_name=self.application_context.configuration.app_cosmos_database,
                collection_name=self.application_context.configuration.app_cosmos_container_schema,
                schema_id=analyzer_id,
            )
            schema_model = load_schema_from_blob(
                account_url=self.application_context.configuration.app_storage_blob_url,
                container_name=f"{self.application_context.configuration.app_cps_configuration}/Schemas/{analyzer_id}",
                blob_name=selected_schema.FileName,
                module_name=selected_schema.ClassName,
            )
            cu_schema = build_content_understanding_schema(schema_model)
            content_understanding_helper.begin_create_analyzer(
                analyzer_id=analyzer_id, analyzer_template=cu_schema
            )

        response = content_understanding_helper.begin_analyze_stream(
            analyzer_id=analyzer_id,
            file_stream=context.data_pipeline.get_source_files()[0].download_stream(
                self.application_context.configuration.app_storage_blob_url,
                self.application_context.configuration.app_cps_processes,
            ),
        )

        response = content_understanding_helper.poll_result(response)
        result: AnalyzedResult = AnalyzedResult(**response)

        # Save Result as a file
        # Create File Entity to add
        result_file = context.data_pipeline.add_file(
            file_name="content_understanding_output.json",
            artifact_type=ArtifactType.ExtractedContent,
        )

        # log for file uploading
        result_file.log_entries.append(
            PipelineLogEntry(
                **{
                    "source": self.handler_name,
                    "message": "Content Understanding Extraction Result has been added",
                }
            )
        )

        # Upload the result to blob storage
        result_file.upload_json_text(
            account_url=self.application_context.configuration.app_storage_blob_url,
            container_name=self.application_context.configuration.app_cps_processes,
            text=result.model_dump_json(),
        )

        return StepResult(
            process_id=context.data_pipeline.pipeline_status.process_id,
            step_name=self.handler_name,
            result={
                "result": "success",
                "file_name": result_file.name,
            },
        )
