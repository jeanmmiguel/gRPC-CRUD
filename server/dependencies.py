from models import  SessionLocal
from sqlalchemy.orm import sessionmaker, Session
from models import User

#from main import bcrypt_context , SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, oauth2_schema
def get_session():
    Session = sessionmaker(bind=db)
    session = Session()
    
    return session
