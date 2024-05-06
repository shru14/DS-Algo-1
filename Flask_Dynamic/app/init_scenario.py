from .extensions import db
from app.models import Configuration


#Creating instance of different configurations 
def init_configurations():
    configs = [
        Configuration(key='even_preferences', value='1'),
        Configuration(key='limited_capacities', value='2'),  
        Configuration(key='uneven_preferences', value='3') 
    ]
    db.session.bulk_save_objects(configs)
    db.session.commit()

if __name__ == '__main__':
    init_configurations()


#function to fetch current configuration 
def get_active_configuration():
    config = Configuration.query.filter_by(key='active_configuration').first()
    if config:
        return config.value
    return None