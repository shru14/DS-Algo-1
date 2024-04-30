from .extensions import db
from flaskapp.models import Configuration

#Creating instance of different configurations 
def init_configurations():
    configs = [
        Configuration(key='even_preferences', value='default'),
        Configuration(key='limited_capacity', value='1'),  
        Configuration(key='uneven_preferences', value='2') 
    ]
    db.session.bulk_save_objects(configs)
    db.session.commit()

if __name__ == '__main__':
    init_configurations()