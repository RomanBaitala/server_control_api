from typing import List, Optional
from passlib.context import CryptContext
from ..interfaces import IUserService
from ...dal.interfaces import IUserRepository
from ...schemas import UserCreate, UserUpdate, UserResponse, UserLogin
from ...models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def register_user(self, user_data: UserCreate) -> UserResponse:
        if self.user_repo.get_by_email(user_data.email):
            raise ValueError(f"Користувач з email {user_data.email} вже існує")

        hashed_password = pwd_context.hash(user_data.password)

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )

        created_user = self.user_repo.create(new_user)
        return UserResponse.model_validate(created_user)
    
    def authenticate_user(self, user_data: UserLogin) -> Optional[UserResponse]:
        user = self.user_repo.get_by_email(user_data.email)
        if not user:
            return None
        
        if not pwd_context.verify(user_data.password, user.password):
            return None
        
        return UserResponse.model_validate(user)

    def get_user_profile(self, user_id: int) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Користувача не знайдено")
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int, update_data: UserUpdate) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Користувача не знайдено")

        data = update_data.model_dump(exclude_unset=True)

        if 'email' in data and data['email'] != user.email:
            if self.user_repo.get_by_email(data['email']):
                raise ValueError("Цей email вже зайнятий іншим користувачем")

        for key, value in data.items():
            setattr(user, key, value)

        updated_user = self.user_repo.update(user)
        return UserResponse.model_validate(updated_user)

    def delete_user(self, user_id: int) -> bool:
        if not self.user_repo.get_by_id(user_id):
            raise ValueError("Користувача не знайдено")
        self.user_repo.delete(user_id)
        return True