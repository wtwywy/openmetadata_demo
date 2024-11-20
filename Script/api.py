"""
    (metadataa of) API
"""
import connection
from metadata.generated.schema.api.services.createApiService import CreateApiServiceRequest
from metadata.generated.schema.entity.services.apiService import ApiServiceConnection
from metadata.generated.schema.entity.services.connections.apiService.restConnection import RESTConnection

def create_api_service(service_name, desc, url):
    bot = connection.get_bot()
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

from metadata.generated.schema.api.data.createAPICollection import CreateAPICollectionRequest
def create_api_collection(collection_name, desc, service_fqn, url):
    bot = connection.get_bot()
    collection = CreateAPICollectionRequest(
        name = collection_name,
        description = desc,
        service = service_fqn,
        endpointURL=url
    )
    collection = bot.create_or_update(collection)
    print(f"Collection '{collection.name}' created successfully!")
    return collection

from metadata.generated.schema.api.data.createAPIEndpoint import CreateAPIEndpointRequest
def create_api_endpoint(endpoint_name, desc, collection_fqn, url):
    bot = connection.get_bot()
    endpoint = CreateAPIEndpointRequest(
        name = endpoint_name,
        description = desc,
        apiCollection=collection_fqn,
        endpointURL=url,
    )
    endpoint = bot.create_or_update(endpoint)
    print(f"Endpoint '{endpoint.name}' created successfully!")
    return endpoint