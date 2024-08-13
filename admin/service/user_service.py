from ..repository.user_repository import select_all,create_user
from ..model.user_model import User

def select_all_user_service():
    users = select_all()
    print(users)
    return users

def create_user_service(username: str, password: str,phone: str,name: str):
    user = select_all_user_service(username)
    if(len(user) == 0):
        user_save = User(username=username, password=password, phone=phone, name=name)
        return create_user(user_save)
    else:
        print('El usuario ya existe')
        raise BaseException('El usuario ya existe')