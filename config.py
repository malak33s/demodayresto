import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mot_de_passe@localhost/demoday_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')  # Clé pour Flask
