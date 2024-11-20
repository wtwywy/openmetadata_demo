from metadata.generated.schema.api.services.createPipelineService import CreatePipelineServiceRequest
from metadata.generated.schema.entity.services.pipelineService import PipelineConnection
from metadata.generated.schema.entity.services.connections.pipeline.airflowConnection import AirflowConnection
from metadata.generated.schema.entity.services.connections.pipeline.backendConnection import BackendConnection
from metadata.generated.schema.entity.services.pipelineService import PipelineConnection
from metadata.generated.schema.entity.services.connections.pipeline.airflowConnection import AirflowConnection
from metadata.generated.schema.entity.services.connections.pipeline.backendConnection import BackendConnection
import connection

def create_airflow_service(service_name, host_port):
    bot = connection.get_bot()
    service = CreatePipelineServiceRequest(
        name=service_name,
        serviceType="Airflow",
        connection=PipelineConnection(
            config=AirflowConnection(
                hostPort=host_port,
                connection=BackendConnection()
            )
        )
    )
    service = bot.create_or_update(service)
    print(f"Service '{service.name}' created successfully!")
    return service