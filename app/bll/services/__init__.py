from .user_service import UserService
from .server_service import ServerService
from .metric_service import MetricService

from ...dal.repositories import user_repository, server_repository, metric_repository

user_service = UserService(user_repository)
server_service = ServerService(server_repository)
metric_service = MetricService(metric_repository, server_repository)