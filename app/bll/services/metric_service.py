from typing import List
from ..interfaces.imetric_service import IMetricService
from ...dal.interfaces import IMetricRepository, IServerRepository
from ...schemas import MetricResponse
from ...models import Metric

class MetricService(IMetricService):
    def __init__(self, metric_repo: IMetricRepository, server_repo: IServerRepository):
        self.metric_repo = metric_repo
        self.server_repo = server_repo

    def add_metric(self, server_id: int, cpu_usage: float, cpu_temp: float, ram_usage: float) -> MetricResponse:
        if not self.server_repo.get_by_id(server_id):
            raise ValueError(f"Сервер з ID {server_id} не знайдено. Метрики відхилено.")

        new_metric = Metric(
            server_id=server_id,
            cpu_usage=cpu_usage,
            cpu_temp=cpu_temp,
            ram_usage=ram_usage
        )

        created_metric = self.metric_repo.create(new_metric)
        return MetricResponse.model_validate(created_metric)

    def get_server_history(self, server_id: int, limit: int = 20) -> List[MetricResponse]:
        metrics = self.metric_repo.get_by_server(server_id)
        
        latest_metrics = metrics[-limit:]
        
        return [MetricResponse.model_validate(m) for m in latest_metrics]