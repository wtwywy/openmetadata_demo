import connection
from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.teams.team import Team
from metadata.generated.schema.entity.data.pipeline import Pipeline
from metadata.generated.schema.entity.data.container import Container
from metadata.generated.schema.entity.data.dashboard import Dashboard

def get_entity_by_name(fqn, type:str):
    """
        return obj
    """
    bot = connection.get_connection_obj()
    if type == 'table':
        entity = bot.get_by_name(entity=Table,fqn=fqn)
    elif type == 'container':
        entity = bot.get_by_name(entity=Container,fqn=fqn)
    elif type == 'pipeline':
        entity = bot.get_by_name(entity=Pipeline,fqn=fqn)
    elif type == 'team':
        entity = bot.get_by_name(entity=Team,fqn=fqn)
    elif type == 'dashboard':
        entity = bot.get_by_name(entity=Dashboard,fqn=fqn)
    else: raise Exception("this type is not support"+type)
    return entity