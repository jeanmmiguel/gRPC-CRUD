from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///users.db", echo=True)

# Session ligada ao engine
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    #comandos sql restricoes sql
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False)
    password =  Column("password", String, nullable=False)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

Base.metadata.create_all(engine)
