from .ibase_repository import IBaseRepository
from ...models import Server
from typing import List, Optional
from abc import abstractmethod

class IServerRepository(IBaseRepository[Server]):
    @abstractmethod
    def get_by_owner(self, owner_id: int) -> List[Server]:
        pass

    @abstractmethod
    def get_by_ip(self, ip_address: str) -> Optional[Server]:
        pass

    @abstractmethod
    def get_all_active(self) -> List[Server]:
        pass
