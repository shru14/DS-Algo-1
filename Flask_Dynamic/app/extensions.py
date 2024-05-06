from flask_sqlalchemy import SQLAlchemy

#Separating initialisation of databse to avoid circular imports 
db = SQLAlchemy()