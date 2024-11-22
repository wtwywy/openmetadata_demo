"""
    uncatagorized code
"""
import yaml

import connection


# pip install "openmetadata-ingestion==1.5.5"

# UI airflow ingestion ต้องการ database connection, เลย skip ไปก่อนแล้วทำ manual ไปก่อน
# clone git and copy airflow_provider_openmetadata ไปที่ ____ airflow/????(script/plugin)

# ไม่ต้องสร้างก็ได้ ถ้าที่ใช้ใน dag ไม่มีมันจะสร้างให้ แล้วได้ connectionUrl แบบ default งั้นสร้างเองดีกว่า
# ไปติดตั้ง plugin เพิ่ม connection
# in dag: use opmtdthook to get serverconfig then use opmtdtoperator (while setup inlets outlest each task)


from metadata.generated.schema.api.teams.createTeam import CreateTeamRequest
def create_team(name, display_name, team_type: str, parent_list: list, description: str = ""):
    ingest_bot = connection.get_connection_obj()
    team = CreateTeamRequest(
        teamType=team_type,
        name=name,
        displayName=display_name,
        parents=parent_list,
        description=description
    )
    team = ingest_bot.create_or_update(team)
    print(f"{team_type} '{name}' created successfully!")
    return team

def create_team_from_yaml(yaml_file_path):
    yaml_data:dict
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    for businessUnit in yaml_data['businessUnits']:
        unit_name=businessUnit["name"]
        display_name=businessUnit.get('displayName')
        description=businessUnit.get('description')
        theUnit = create_team(unit_name, display_name, "BusinessUnit", None, description)
        if 'departments' in businessUnit:
            for department in businessUnit['departments']:  # for each column    
                department_name=department["name"]
                display_name=department.get('displayName')
                description=department.get('description')
                theDepartment = create_team(department_name, display_name, "Department", [theUnit.id], description)
                if 'groups' in department:
                    for group in department['groups']:
                        group_name=group["name"]
                        display_name=group.get('displayName')
                        description=group.get('description')
                        create_team(group_name, display_name, "Group", [theDepartment.id], description)

from metadata.generated.schema.api.teams.createUser import CreateUserRequest
def create_user(name, displayName, email, desc='', team_list=None, role_list=None):
    ingest_bot = connection.get_connection_obj()
    user = CreateUserRequest(
        name=name,
        displayName=displayName,
        description=desc,
        email=email,
        teams=team_list,
        roles=role_list,
    )
    user = ingest_bot.create_or_update(user)
    print(f"User '{name}' created successfully!")
    return user

from metadata.generated.schema.auth.basicAuth import BasicAuthMechanism
from metadata.generated.schema.entity.teams.user import AuthenticationMechanism
def create_user_with_password(name, displayName, email, password, desc='', team_list=None, role_uuid_list=None):
    ingest_bot = connection.get_bot()
    user = CreateUserRequest(
        name=name,
        displayName=displayName,
        description=desc,
        email=email,
        authenticationMechanism=AuthenticationMechanism(
            config=BasicAuthMechanism(
                password=password
            ),
            authType='BASIC',
        ),
        createPasswordType='ADMIN_CREATE',
        password=password,
        confirmPassword=password,
        teams=team_list,
        roles=role_uuid_list,
    )
    user = ingest_bot.create_or_update(user)
    print(f"User '{name}' created successfully!")
    return user


from metadata.generated.schema.entity.teams.team import Team
from metadata.generated.schema.entity.teams.role import Role
def create_user_from_yaml(yaml_file_path):
    yaml_data:list
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    bot = connection.get_connection_obj()
    
    user:dict
    for user in yaml_data:
        name=user["name"]
        display_name=user["displayName"]
        desc=user.get("description")
        email=user["email"]
        team_list=[]
        role_list=[]
        if 'teams' in user:
            for team_fqn in user['teams']:
                team_id = bot.get_by_name(entity=Team, fqn=team_fqn).id
                team_list.append(team_id)
        if 'roles' in user:
            for role_fqn in user['roles']:
                role_id = bot.get_by_name(entity=Role, fqn=role_fqn).id
                role_list.append(role_id)
        create_user(
            name=name,
            displayName=display_name,
            email=email,
            desc=desc if desc else None,
            team_list=team_list if team_list else None,
            role_list=role_list if role_list else None,
        )