#define opm Openmetadata


step
  - build docker
  - get bot token put in code and airflow cfg
  - run script (setup.py)
  - create ingestion pipeline and run
    - metadata
    - profiler
  - run dag (ETL airflow)
  - run script (create_lineage.py)


how to install opm
  1. download docker compose file
  2. docker-compose up -d 


how to install sdk
  1. Install python
  2. Install required module/plackage/library
    "pip install -r requirements.txt"


how to init the demo
  - run setup code
  - in opm ui, ingest db table
  - in airflow run dag (with [lineage] config'ed)
  - run create_lineage


how to update opm:
  1. backup(I didn't learn yet)
  2. download docker_compose file from git
  3. replace compose file 
  4. compose

note for self:
  setup the metadata:
    most of the setup job sure can be SDK'ed 
    by create method that read file and use SDK/api to push to opm
    then collecting most setup data users in org
    then datacatalog team use the collected data to setup opm project
  
  as some metadata/ functionality of opm cant be set via SDK now we still need to use GUI

  then after setup phase, when new data come:
  - GUI is good option to work aroud some small change of metadata, create new ingestion pipeline, new user, new team
  - file+SDK is still a good way  
    - and I recommend to append new data and keep the old data file
  


  then airflow lineage as of now I create program to read yaml


how to upload DAG to opm?y
  1. set [lineage] config in airflow.cfg
  backend = script.airflow_provider_openmetadata.lineage.backend.OpenMetadataLineageBackend
  airflow_service_name = local_airflow
  openmetadata_api_endpoint = http://host.docker.internal:8585/api
  jwt_token = eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImluZ2VzdGlvbi1ib3QiLCJyb2xlcyI6WyJJbmdlc3Rpb25Cb3RSb2xlIl0sImVtYWlsIjoiaW5nZXN0aW9uLWJvdEBvcGVuLW1ldGFkYXRhLm9yZyIsImlzQm90Ijp0cnVlLCJ0b2tlblR5cGUiOiJCT1QiLCJpYXQiOjE3MjY4MTc1NTcsImV4cCI6bnVsbH0.Sok4F0YmdYFwyLLn9xLctOoPGh31rL6eonyWFENDBywjoG5Dv0KMiMHkDtYibP6CmVIPnw3lZAajdLd0_AEeOszcvq0SdoyM8zS_UulbSqQ8IpeChqKxf7nxHMX9a2-I43iVrh_ZcVMPVBbVrr8jI5sC-KdftsBkxjl9tn_N6cZHyN2w2sA9AhtO31LlCnyj-P7teV_h5SrRLp8OWMTPxAcZe3FdsKzb-2uWXO4lNXtD4p1E6lgYxkL-ejPtg-xji-5ztWybKDBLk6bzFkHl7CVyAXLl1Vf0JHDM6b5b8nkH-yXlWhHbwS2viesLb5_bktn3KiyGpLQwG_f0X4KZwQ
  2. user opm operator as a task inside DAG
  from airflow_provider_openmetadata.lineage.operator import OpenMetadataLineageOperator
  from airflow_provider_openmetadata.hooks.openmetadata import OpenMetadataHook
  openmetadata_hook = OpenMetadataHook(openmetadata_conn_id="openmetadata")  # The ID you provided
  server_config = openmetadata_hook.get_conn()
  opm = OpenMetadataLineageOperator(
      task_id='lineage_op',
      depends_on_past=False,
      server_config=server_config,
      service_name="local_airflow",
  )


how to get airflow dag's metadata:
  1. download airflow_provider_openmetadata from github
    and put somewhere in airflow project (for me /scripts)
  2. set [lineage] in airflow.dfg example:
    backend = script.airflow_provider_openmetadata.lineage.backend.OpenMetadataLineageBackend
    airflow_service_name = local_airflow
    openmetadata_api_endpoint = http://host.docker.internal:8585/api
    jwt_token = qazwsxedcrfvtgbyhnujmik
  3. run the dag

users?
  - now i cant create user with any auth method (i dont know what i am missing) but can with email, role, team
  - let user create new paswd later when login (forgot password)

uninstall?
  - have trying delete local file
  - at now after re compose the docker file I still see some data in explore page (but i cant go into that data asset)
  - mysql
    mysql --user=root --password=password --silent --execute "use openmetadata_db; DROP DATABASE openmetadata_db;"
    mysql --user=root --password=password --silent --execute "use openmetadata_db; DROP DATABASE airflow_db;"
  - elastic
    curl -X PUT "http://localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
    {
      "persistent": {
        "action.destructive_requires_name": "false"
      }
    }'

    curl -X DELETE "http://localhost:9200/*"

    curl -X PUT "http://localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
    {
      "persistent": {
        "action.destructive_requires_name": "true"
      }
    }'






