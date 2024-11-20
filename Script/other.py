"""
    non library
"""
import requests
import yaml
import json
from dotenv import load_dotenv
from Script import entity

with open("Config/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
BASE_URL = config['api_endpoint']

headers = {
    "Authorization": f"Bearer {config['ingest_bot_token']}",
    "Content-Type": "application/json"
}

def get_all_tables(object:bool = False):
    url = f"{BASE_URL}/v1/tables"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tables = response.json()
        with open('Output/list_table.json', "w") as file:
            json.dump(tables, file, indent=4)
        
        if object:
            table_obj = []
            for table in tables['data']:
                table_obj.append(entity.get_entity_by_name(table['fullyQualifiedName'],'table'))
            return table_obj
        else:
            return tables
    
    except requests.exceptions.HTTPError as err:
        print(f"Failed to fetch tables: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_all_pipeline(object:bool = False):
    url = f"{BASE_URL}/v1/pipelines"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        pipelines = response.json()
        with open('Output/list_pipeline.json', "w") as file:
            json.dump(pipelines, file, indent=4)
        
        if object:
            pipeline_obj = []
            for pipeline in pipelines['data']:
                pipeline_obj.append(entity.get_entity_by_name(pipeline['fullyQualifiedName'],'table'))
            return pipeline_obj
        else:
            return pipelines
    
    except requests.exceptions.HTTPError as err:
        print(f"Failed to fetch pipelines: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_edges_from_entity_fqn(entity, fqn):
    url = f"{BASE_URL}/v1/lineage/{entity}/name/{fqn}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        edges = response.json() 
        with open('Output/edge.json', "w") as file:
            json.dump(edges, file, indent=4)
        return edges
    
    except requests.exceptions.HTTPError as err:
        print(f"Failed to fetch edges: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def get_all_policy():
    url = f"{BASE_URL}/v1/policies"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        policies = response.json()
        with open('Output/last_policy.json', "w") as file:
            json.dump(policies, file, indent=4)
        return policies
    
    except requests.exceptions.HTTPError as err:
        print(f"Failed to fetch policies: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_db_service(service_name):
    url = f"{BASE_URL}/v1/services/databaseServices/name/{service_name}"
    params = {
        "hardDelete": True,
        #"recursive": True
    }
    response = requests.delete(url, headers=headers, params=params)
    if response.status_code == 200:
        print(f"Successfully deleted database service '{service_name}'")
    else:
        print(f"Failed to delete database service '{service_name}': {response.status_code}")
        print(response.json())

def get_all_database_service():
    url = f"{BASE_URL}/v1/services/databaseServices"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        entities = response.json()
        with open('Output/last_dbs.json', "w") as file:
            json.dump(entities, file, indent=4)
        return entities
    
    except requests.exceptions.HTTPError as err:
        print(f"Failed to fetch: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_glossary():
    url = f"{BASE_URL}/v1/glossaryTerms"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        entities = response.json()
        with open('Output/list_glossary.json', "w") as file:
            json.dump(entities, file, indent=4)
        return entities
    
    except requests.exceptions.HTTPError as err:
        print(f"Failed to fetch: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_asset_to_glossary_term(id, asset_id, asset_type):
    url = f"{BASE_URL}/v1/glossaryTerms/{id}/assets/add"
    params = {
        "assets": [
            {
                "id": asset_id,
                "type": asset_type
            }
        ]
    }
    try:
        response = requests.put(url, headers=headers, json=params)
        response.raise_for_status()
        entities = response.json()
        with open('Output/other_response.json', "w") as file:
            json.dump(entities, file, indent=4)
        return entities
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
import requests
import json
def add_tag_to_table(fqn):
    """
        original code from dev on slack 
        https://openmetadata.slack.com/archives/C02B6955S4S/p1727162956035739?thread_ts=1727161805.111059&cid=C02B6955S4S
    """
    # Define the API endpoint and headers
    url = f"{BASE_URL}/v1/tables/name/{fqn}"
    # Define the payload to add a glossary term to a column
    payload = [
        {
            "op": "add",
            "path": "/columns/0/tags/0",
            "value": {
                "tagFQN": "first_glos.term",
                "name": "term",
                "source": "Glossary"
            }
        }
    ]
    # Make the API request
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        entities = response.json()
        with open('Output/other_response.json', "w") as file:
            json.dump(entities, file, indent=4)
        return entities
    except Exception as e:
        print(f"An error occurred: {e}")

c2waccount = "ee485689-0894-4e4b-9296-f73758c85bec"
add_tag_to_table("DWH.SetDB.dbo.C2WAccount")


#get_all_tables()
#list_glossary()
#add_asset_to_glossary_term("da99210a-0a6b-44b4-868c-456761dc3537", asset_id="ee485689-0894-4e4b-9296-f73758c85bec", asset_type="Table")

#print(get_edges_from_entity_fqn('table',"DWH.SetDB.dbo.C2WPort"))
#get_edges_from_entity_fqn()
#print(get_all_policy())
#dbs = get_all_database_service()
#for db in dbs['data']:
#    print(db['name'])
#delete_db_service('abcdef')
#print(dbs)