"""
    policy, rule, role
"""
import connection
import yaml
from metadata.generated.schema.api.policies.createPolicy import CreatePolicyRequest
from metadata.generated.schema.entity.policies.accessControl.rule import Rule
from metadata.generated.schema.api.teams.createRole import CreateRoleRequest

def create_policy(name, display_name, description, rules):
    bot = connection.get_connection_obj()
    policy = CreatePolicyRequest(
        name=name,
        displayName=display_name,
        description=description,
        rules=rules
    )
    policy = bot.create_or_update(policy)
    print(f"Policy '{name}' created successfully!")
    return policy
def create_policy_from_yaml(yaml_file_path):
    yaml_data:list
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    policy: dict
    for policy in yaml_data:
        if 'rules' in policy:
            rules = []
            rule:dict
            for rule in policy['rules']:
                rule = Rule(
                    name = rule['name'],
                    description = rule['description'],
                    effect=rule['effect'],
                    operations=rule['operations'],
                    resources=rule['resources'],
                    condition=rule['condition']
                )
                rules.append(rule)
        create_policy(
            policy.get('name'), policy.get('displayName'), policy.get('description'), rules
        )

def create_role(name:str, display_name:str, description:str, policies:list):
    bot = connection.get_connection_obj()
    role = CreateRoleRequest(
        name=name,
        displayName=display_name,
        description=description,
        policies=policies
    )
    role = bot.create_or_update(role)
    print(f"Role '{name}' created successfully!")
    return role

def create_role_from_yaml(yaml_file_path):
    yaml_data:list
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    role: dict
    for role in yaml_data:
        create_role(
            name= role.get('name'),
            display_name=role.get('displayName'),
            description=role.get('description'),
            policies=role.get('policies')
        )