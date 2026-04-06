from .user_service import UserService
from .server_service import ServerService

from ...dal.repositories import user_repository, server_repository

user_service = UserService(user_repository)
server_service = ServerService(server_repository) 