from abc import ABC, abstractmethod
from typing import List
from ...schemas import MetricResponse

class IMetricService(ABC):
    @abstractmethod
    def add_metric(self, server_id: int, cpu_usage: float, cpu_temp: float, ram_usage: float) -> MetricResponse:
        pass

    @abstractmethod
    def get_server_history(self, server_id: int, limit: int = 20) -> List[MetricResponse]:
        pass