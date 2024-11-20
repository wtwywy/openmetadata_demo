import connection
from metadata.generated.schema.entity.services.databaseService import DatabaseServiceType, DatabaseConnection
from metadata.generated.schema.entity.services.connections.database.mssqlConnection import MssqlConnection
from metadata.generated.schema.api.services.createDatabaseService import CreateDatabaseServiceRequest
def create_mssql_service(service_name, connection_details):
    bot = connection.get_bot()
    sql_connection = DatabaseConnection(
        config=MssqlConnection(**connection_details)
    )
    service = CreateDatabaseServiceRequest(
        name=service_name,
        serviceType=DatabaseServiceType.Mssql,
        connection=sql_connection
    )
    service = bot.create_or_update(service)
    print(f"Service '{service.name}' created successfully!")
    return service.id

from metadata.generated.schema.api.data.createStoredProcedure import CreateStoredProcedureRequest
from metadata.generated.schema.entity.data.storedProcedure import StoredProcedureCode
def create_stored_procedure(name,desc,lang,code,databaseSchema):
    bot = connection.get_bot()
    procedure = CreateStoredProcedureRequest(
        name=name,
        description=desc,
        storedProcedureCode=StoredProcedureCode(
            language = lang,
            code = code
        ),
        databaseSchema=databaseSchema
    )
    procedure = bot.create_or_update(procedure)
    print(f"Procedure '{name}' created successfully!")
    return procedure