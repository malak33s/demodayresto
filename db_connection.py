from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connexion à MySQL
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_NAME = "demoday_db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)
