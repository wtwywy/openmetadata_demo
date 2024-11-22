"""
    connection obj
"""
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection, AuthProvider,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import OpenMetadataJWTClientConfig
import yaml

with open("Config/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

metadata = None
def get_connection_obj():
    global metadata
    if metadata is None:
        server_config = OpenMetadataConnection(
            hostPort="http://localhost:8585/api",
            authProvider=AuthProvider.openmetadata,
            securityConfig=OpenMetadataJWTClientConfig(
                jwtToken=config['ingest_bot_token']
            ),
        )
        metadata = OpenMetadata(server_config)
    return metadata

def get_token():
    return config['ingest_bot_token']

def check_health():
    global metadata
    if metadata.health_check():
        print("connected")
    else:
        print("not connected")
