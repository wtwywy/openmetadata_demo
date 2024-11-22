"""
    dashboard
"""
import connection
import yaml
from metadata.generated.schema.api.services.createDashboardService import CreateDashboardServiceRequest   
from metadata.generated.schema.api.data.createDashboard import CreateDashboardRequest
from metadata.generated.schema.api.data.createChart import CreateChartRequest 

def create_dashboard_service(name, displayName, desc, service_type):
    bot = connection.get_connection_obj()
    service = CreateDashboardServiceRequest(
        name = name,
        displayName=displayName,
        description = desc,
        serviceType = service_type,
    )
    service = bot.create_or_update(service)
    print(f"dashboard service '{name}' created successfully!")
    return service

def create_dashboard(name, displayName, desc, service_fqn):
    bot = connection.get_connection_obj()
    dashboard = CreateDashboardRequest(
        name = name,
        displayName=displayName,
        description = desc,
        service=service_fqn,
    )
    dashboard = bot.create_or_update(dashboard)
    print(f"dashboard '{name}' created successfully!")
    return dashboard

def create_chart(name, displayName, desc, chartType, service_fqn, dashboard_fqns=None):
    bot = connection.get_connection_obj()
    chart = CreateChartRequest(
        name = name,
        displayName=displayName,
        description = desc,
        chartType=chartType,
        service=service_fqn,
        dashboards=dashboard_fqns,
    )
    chart = bot.create_or_update(chart)
    print(f"chart '{name}' created successfully!")
    return chart

def create_dashboard_from_yaml(yaml_file_path):
    yaml_data:dict
    with open(yaml_file_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    
    for serviceType, services in yaml_data.items():
        service: dict
        for service in services:
            service_fqn = service.get('name')
            create_dashboard_service(
                name=service_fqn,
                displayName=service.get('displayName'),
                desc=service.get('description'),
                service_type=serviceType,
            )
            if 'dashboards' in service:
                dashboard: dict
                for dashboard in service['dashboards']:
                    dashboard_fqn = dashboard.get('name')
                    create_dashboard(
                        name=dashboard_fqn,
                        displayName=dashboard.get('displayName'),
                        desc=dashboard.get('description'),
                        service_fqn=service.get('name'),
                    )
                    if 'charts' in dashboard:
                        chart:dict
                        for chart in dashboard['charts']:
                            create_chart(
                                name=chart.get('name'),
                                displayName=chart.get('displayName'),
                                desc=chart.get('description'),
                                chartType=chart.get('chartType'),
                                service_fqn=service_fqn,
                                dashboard_fqns=[service_fqn+'.'+dashboard_fqn],
                            )
