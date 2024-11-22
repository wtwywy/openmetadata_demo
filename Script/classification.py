"""
    tag, business glossary
"""
import connection
import yaml
import entity
from metadata.ingestion.models.table_metadata import ColumnTag
from metadata.generated.schema.type.tagLabel import TagLabel
from metadata.ingestion.ometa.mixins.patch_mixin_utils import PatchOperation
from metadata.generated.schema.api.classification.createClassification import CreateClassificationRequest
from metadata.generated.schema.api.classification.createTag import CreateTagRequest
from metadata.generated.schema.api.data.createGlossary import CreateGlossaryRequest
from metadata.generated.schema.api.data.createGlossaryTerm import CreateGlossaryTermRequest

def create_classification(name, displayName, description, mutuallyExclusive):
    bot = connection.get_connection_obj()
    classification = CreateClassificationRequest(
        name=name,
        displayName=displayName or None,
        description=description or '',
        mutuallyExclusive=mutuallyExclusive or None,
    )
    classification = bot.create_or_update(classification)
    print(f"classification '{name}' created successfully!")
    return classification

def create_tag(name, display_name, desc, classification_fqn:str =None):
    bot = connection.get_connection_obj()
    tag = CreateTagRequest(
        name=name,
        displayName=display_name or None,
        description=desc or '',
        classification=classification_fqn if classification_fqn else None,
    )
    tag = bot.create_or_update(tag)
    print(f"Tag '{name}' created successfully!")
    return tag

def create_classification_tag_from_yaml(yaml_file_path):
    yaml_data:list
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    
    classification:dict
    for classification in yaml_data: #for each service in file
        classif_name=classification['name']
        classif_displayName=classification.get("displayName")
        classif_desc=classification.get("description")
        classif_mutuallyExclusive=classification.get("mutuallyExclusive")
        create_classification(
            name=classif_name,
            displayName=classif_displayName or None,
            description=classif_desc or '',
            mutuallyExclusive=classif_mutuallyExclusive or None,
        )
        if 'tags' in classification:
            tag:dict
            for tag in classification['tags']:
                name = tag['name']
                display_name = tag.get('displayName')
                description = tag.get('description')
                create_tag(
                    name=name,
                    display_name=display_name or None,
                    desc=description or '',
                    classification_fqn= classif_name
                )
                
def create_business_glossary(name, display_name, description):
    bot = connection.get_connection_obj()
    glos = CreateGlossaryRequest(
        name = name,
        displayName=display_name,
        description=description,
    )
    glos = bot.create_or_update(glos)
    print(f"Business glossary '{name}' created successfully!")
    return glos

def create_glossary_term(glos_fqn, name, display_name,description):
    bot = connection.get_connection_obj()
    glos = CreateGlossaryTermRequest(
        glossary=glos_fqn,
        name = name,
        displayName=display_name,
        description=description,
    )
    glos = bot.create_or_update(glos)
    print(f"Business glossary '{name}' created successfully!")
    return glos

def create_glossary_term_from_file(yaml_file_path):
    yaml_data:list
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    
    glossaries:dict
    for glossaries in yaml_data:
        glos_name = glossaries.get('name')
        create_business_glossary(
            name=glos_name,
            display_name=glossaries.get('displayName') or None,
            description=glossaries.get('description') or ''
        )
        if 'terms' in glossaries:
            term:dict
            for term in glossaries['terms']:
                create_glossary_term(
                    glos_fqn=glos_name,
                    name=term.get('name'),
                    display_name=term.get('displayName') or None,
                    description=term.get('description') or ''
                )

def assign_tag_to_column_from_yaml(yaml_file_path):
    yaml_data:dict
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    conn = connection.get_connection_obj()
    
    databases:dict
    for service_name, databases in yaml_data.items():
        schemas:dict
        for database_name, schemas in databases.items():
            tables:dict
            for schema_name, tables in schemas.items():
                columns:list
                for table_name, columns in tables.items():
                    table_fqn = '.'.join((service_name, database_name, schema_name, table_name))
                    print("table_fqn")
                    column:dict
                    tag_list=[]
                    for column in columns:
                        column_name = column.get('name')
                        column_fqn=table_fqn+'.'+column_name
                        print(f"-- {column_name}")
                        if ('tags' not in column) and ( 'terms' not in column):
                            raise Exception('column got no terms / tags')
                        if 'tags' in column:
                            for tag in column['tags']:
                                tag_label = TagLabel(
                                    tagFQN=tag,
                                    source='Classification', # 'Glossary'
                                    labelType='Manual', #'Propagated' 'Automated' 'Derived'
                                    state='Confirmed' # 'Suggested'
                                )
                                tag_list.append(ColumnTag(column_fqn=column_fqn, tag_label=tag_label))
                        if 'terms' in column:
                            for term in column['terms']:
                                tag_label = TagLabel(
                                    tagFQN=term,
                                    source='Glossary',
                                    labelType='Manual',
                                    state='Confirmed'
                                )
                                tag_list.append(ColumnTag(column_fqn=column_fqn, tag_label=tag_label))
                    table_obj = entity.get_entity_by_name(table_fqn,'table')
                    conn.patch_column_tags(
                        table=table_obj,
                        column_tags=tag_list,
                        operation=PatchOperation.ADD
                    )
    