"""
    data lineage
"""
import yaml
import connection
from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.type.entityLineage import EntitiesEdge, LineageDetails, ColumnLineage
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.generated.schema.type.basic import SqlQuery
import entity


def add_lineage_edge(pipeline_id, source_type, source_fqn, dest_type, dest_fqn, description, col_lineage_list, sqlQuery):
    bot = connection.get_connection_obj()
    source_id = entity.get_entity_by_name(source_fqn, source_type).id
    dest_id = entity.get_entity_by_name(dest_fqn, dest_type).id
    lineage=AddLineageRequest(
        edge=EntitiesEdge(
            fromEntity=EntityReference(
                id=source_id,
                type=source_type
            ),
            toEntity=EntityReference(
                id=dest_id,
                type=dest_type
            ),
            lineageDetails=LineageDetails(
                description=description,
                columnsLineage=col_lineage_list,
                pipeline=EntityReference(
                    id=pipeline_id,
                    type="pipeline"
                ),
                sqlQuery=SqlQuery(sqlQuery)
            )
        )
    )
    lineage = bot.add_lineage(lineage)
    return lineage

def add_lineage_from_yaml(yaml_file_path):
    yaml_data:dict
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    service_name:str
    pipelines:dict
    for service_name, pipelines in yaml_data.items(): #for each service in file
        print(f"Processing airflow pipeline: {service_name}")
        pipeline_name:str
        edge_list:list
        for pipeline_name, edge_list in pipelines.items(): #for each pipeline in service
            print(f"Processing pipeline: {pipeline_name}")
            pipeline_id = entity.get_entity_by_name(service_name + '.' + pipeline_name, "pipeline").id
            edge:dict
            for edge in edge_list: # for each table-edge
                source_type = edge['source_type']
                dest_type = edge['dest_type']
                source_fqn = edge['source_fqn']
                dest_fqn = edge['dest_fqn']
                description = edge.get('description', '')
                sql_query = edge.get('sql_query')
                col_lineage_list = []
                if 'column_lineages' in edge:
                    for col in edge['column_lineages']:  # for each column-edge
                        col_lineage = ColumnLineage(
                            fromColumns = [f"{source_fqn}.{col}" for col in col['fromColumns']],
                            toColumn=dest_fqn+'.'+col['toColumn']
                        )
                        col_lineage_list.append(col_lineage)
                add_lineage_edge(
                    pipeline_id=pipeline_id,
                    source_type=source_type,
                    source_fqn=source_fqn,
                    dest_type=dest_type,
                    dest_fqn=dest_fqn,
                    description=description,
                    col_lineage_list=col_lineage_list if col_lineage_list else None,
                    sqlQuery=sql_query if sql_query else ''
                )
