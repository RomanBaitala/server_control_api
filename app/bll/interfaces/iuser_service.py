from abc import ABC, abstractmethod

class IUserService(ABC):
    @abstractmethod
    def register_user(self, name: str, email: str, password: str):
        pass

    @abstractmethod
    def get_user_profile(self, user_id: int):
        pass

    @abstractmethod
    def authenticate_user(self, email: str, password: str):
        pass

    @abstractmethod
    def update_user(self):
        pass 

    @abstractmethod
    def delete_user(self, user_id: int):
        pass