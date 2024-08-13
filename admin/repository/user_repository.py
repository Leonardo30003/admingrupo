from ..model.user_model import User
from .connect_db import connect
from sqlmodel import Session, select



def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(User)
        return session.exec(query).all()
    
def create_user(user:User):
    engine = connect()
    with Session(engine) as session:
        session.add(user)
        session.commit()
        query = select(User)
        return session.exec(query).all()
