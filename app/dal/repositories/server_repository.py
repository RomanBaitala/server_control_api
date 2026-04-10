from .base_repository import BaseRepository
from ..interfaces import IServerRepository
from ...models import Server
from typing import List, Optional

class ServerRepository(BaseRepository[Server], IServerRepository):
    def __init__(self):
        super().__init__(Server)

    def get_by_owner(self, owner_id: int) -> List[Server]:
        return self.model.query.filter_by(owner_id=owner_id).all()

    def get_by_ip(self, ip_address: str) -> Optional[Server]:
        return self.model.query.filter_by(ip_address=ip_address).first()
    
    def get_all_active(self) -> List[Server]:
        return self.model.query.filter_by(status='connected').all()