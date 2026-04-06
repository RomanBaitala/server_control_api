from .ibase_repository import IBaseRepository
from ...models import Metric
from typing import List, Optional
from abc import abstractmethod

class IMetricRepository(IBaseRepository[Metric]):
    @abstractmethod
    def get_by_server(self, server_id: int) -> List[Metric]:
        pass

    @abstractmethod
    def get_latest_by_server(self, server_id: int) -> Optional[Metric]:
        pass
