from Script import (
    connection, dashboard
)

bot = connection.get_connection_obj()
connection.check_health()
api_base = "http://localhost:8585"


#################################
# สร้าง tag และ bussiness glossary
from Script import classification
classification.create_classification_tag_from_yaml('Data/entity/classification.yaml')
classification.create_glossary_term_from_file('Data/entity/glossary.yaml')
#################################



#################################
# สร้าง policy role
from Script import accessControl
accessControl.create_policy_from_yaml('Data/entity/policy.yaml')
accessControl.create_role_from_yaml('Data/entity/role.yaml')
#################################



#################################
# สร้าง team, user
## Organization, BusinessUnit, Division, Department 
from Script import user_team
user_team.create_team_from_yaml('Data/entity/team.yaml')
user_team.create_user_from_yaml('Data/entity/user.yaml')
#################################



#################################
# สร้าง tag และ bussiness glossary
from Script import database
import yaml
yaml_data:dict
with open('Config/config.yaml', "r") as file:
    yaml_data = yaml.safe_load(file)
connection_details = {
    "hostPort": yaml_data['mssql_connection_detail']['hostPort'],
    "username": yaml_data['mssql_connection_detail']['username'],
    "password": yaml_data['mssql_connection_detail']['password'],
    "database": yaml_data['mssql_connection_detail']['database'],
}
service_uuid = database.create_mssql_service("DWH", connection_details)
#################################



#################################
# สร้าง airflow service
from Script import pipeline
service_name = "local_airflow"
host_port = "https://host.docker.internal:8880"
pipeline.create_airflow_service(service_name, host_port)
#################################



#################################
# สร้าง dashboard, chart จากไฟล์
from Script import dashboard
dashboard.create_dashboard_from_yaml('Data/entity/dashboard.yaml')
#################################



#################################
# สร้าง api
from Script import api
api_service = api.create_api_service("sdkApiService", desc="create from sdk python code", url="https://someapi")
collection = api.create_api_collection("collection1", "what is this",api_service.fullyQualifiedName, url="https://someapi/collection1")
api.create_api_endpoint("getSomething", "some endpoint", collection.fullyQualifiedName, url="https://someapi/collection1/getSomething")
api.create_api_endpoint("getFileB", "some endpoint", collection.fullyQualifiedName, url="https://someapi/collection1/getFileB")
#################################



#################################
# สร้าง storage service เพื่อใช้แทนไฟล์
from Script import storage
storage.create_storage_service("FileStorage", "file storage service created from SDK", "CustomStorage")
storage.create_containner_from_yaml('Data/entity/file.yaml')
#################################
