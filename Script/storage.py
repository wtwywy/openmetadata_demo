import connection
import yaml
from metadata.generated.schema.api.services.createStorageService import CreateStorageServiceRequest
from metadata.generated.schema.entity.services.storageService import StorageService
from metadata.generated.schema.entity.data.container import ContainerDataModel
from metadata.generated.schema.api.data.createContainer import CreateContainerRequest
from metadata.generated.schema.entity.data.table import Column

def create_storage_service(service_name, desc, service_type):
    bot = connection.get_bot()
    service = CreateStorageServiceRequest(
        name=service_name,
        description=desc,
        serviceType=service_type,
    )
    service = bot.create_or_update(service)
    print(f"Service '{service.name}' created successfully!")
    return service
def get_storage_service_fqn_by_uuid(uuid):
    bot = connection.get_bot()
    service = bot.get_by_id(
        entity=StorageService,
        entity_id=uuid
    )
    return service.fullyQualifiedName

def create_container(name: str,displayName: str, service_fqn: str, column_list:list ,desc: str = ""):
    ingest_bot = connection.get_bot()
    container = CreateContainerRequest(
        name=name,
        displayName=displayName,
        description=desc,
        service=service_fqn,
        dataModel=ContainerDataModel(
            columns=column_list
        )
    )
    container = ingest_bot.create_or_update(container)
    print(f"Container '{container.name}' created successfully!")
    return container

def create_containner_from_yaml(yaml_file_path):
    """
        read yaml file
    """
    yaml_data:dict
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    bot = connection.get_bot()
    
    service_name:str
    containers:list
    for service_name, containers in yaml_data.items(): #for each service in file
        print(f"Processing from storage service: {service_name}")
        for container in containers: #for each container
            print(f"Processing container: {container['file_name']}")
            service_fqn=service_name
            file_name=container['file_name']
            display_name=container.get('display_name')
            description=container.get('description')
            column_list=[]
            if 'columns' in container:
                    for column in container['columns']:  # for each column
                        column = Column(
                            name=column['name'],
                            dataType=column['data_type'],
                            description=column.get('description'),
                        )
                        column_list.append(column)
            create_container(
                name=file_name,
                displayName=display_name,
                service_fqn=service_fqn,
                column_list=column_list if column_list else None,
                desc=description,
            )