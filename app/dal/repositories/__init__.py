from .server_repository import ServerRepository
from .user_repository import UserRepository
from .metric_repository import MetricRepository

user_repository = UserRepository()
server_repository = ServerRepository()
metric_repository = MetricRepository()
