from .base_repository import BaseRepository
from ..interfaces import IMetricRepository
from ...models import Metric
from typing import List, Optional

class MetricRepository(BaseRepository[Metric], IMetricRepository):
    def __init__(self):
        super().__init__(Metric)

    def get_by_server(self, server_id: int) -> List[Metric]:
        return self.model.query.filter_by(server_id=server_id).all()

    def get_latest_by_server(self, server_id: int) -> Optional[Metric]:
        return self.model.query.filter_by(server_id=server_id).order_by(self.model.timestamp.desc()).first()