"""
    (metadata) API
"""
import connection
from metadata.generated.schema.api.services.createApiService import CreateApiServiceRequest
from metadata.generated.schema.entity.services.apiService import ApiServiceConnection
from metadata.generated.schema.entity.services.connections.apiService.restConnection import RESTConnection
from metadata.generated.schema.api.data.createAPICollection import CreateAPICollectionRequest
from metadata.generated.schema.api.data.createAPIEndpoint import CreateAPIEndpointRequest

def create_api_service(service_name, desc, url):
    """
        สร้าง service
    """
    bot = connection.get_connection_obj()
    service = CreateApiServiceRequest(
        name=service_name,
        serviceType="REST",# | WEBHOOK
        description=desc,
        connection=ApiServiceConnection(
            config=RESTConnection(
                openAPISchemaURL=url
            )
        )
    )
    service = bot.create_or_update(service)
    print(f"Service '{service.name}' created successfully!")
    return service

def create_api_collection(collection_name, desc, service_fqn, url):
    """
        สร้าง api collection (children of api service)
    """
    bot = connection.get_connection_obj()
    collection = CreateAPICollectionRequest(
        name = collection_name,
        description = desc,
        service = service_fqn,
        endpointURL=url
    )
    collection = bot.create_or_update(collection)
    print(f"Collection '{collection.name}' created successfully!")
    return collection

def create_api_endpoint(endpoint_name, desc, collection_fqn, url):
    """
        สร้าง api endpoint (children of api collection)
    """
    bot = connection.get_connection_obj()
    endpoint = CreateAPIEndpointRequest(
        name = endpoint_name,
        description = desc,
        apiCollection=collection_fqn,
        endpointURL=url,
    )
    endpoint = bot.create_or_update(endpoint)
    print(f"Endpoint '{endpoint.name}' created successfully!")
    return endpoint