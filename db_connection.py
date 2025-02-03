from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connexion à la base de données MySQL
engine = create_engine("mysql+mysqlclient://<username>:<password>@localhost/<dbname>")

# Créer une session
Session = sessionmaker(bind=engine)
session = Session()

# Base pour déclarer les classes ORM
Base = declarative_base()

# Exemple de classe pour une table
class TableExample(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

# Créer les tables
Base.metadata.create_all(engine)
