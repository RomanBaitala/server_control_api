from datetime import datetime, timezone, timedelta
from typing import List, Optional
from ...models import Server
from ..interfaces import IServerService
from ...dal.interfaces import IServerRepository
from ...schemas import ServerCreate, ServerResponse, ServerUpdate

class ServerService(IServerService):
    def __init__(self, server_repo: IServerRepository):
        self.server_repo = server_repo

    def create_server(self, owner_id: int, server_data: ServerCreate) -> ServerResponse:
        existing = self.server_repo.get_by_ip(server_data.ip_address)
        if existing:
            raise ValueError(f"Сервер з IP {server_data.ip_address} вже зареєстровано.")

        new_server = Server(
            name=server_data.name,
            ip_address=server_data.ip_address,
            owner_id=owner_id,
            status="active"
        )

        created_server = self.server_repo.create(new_server)
        
        return ServerResponse.model_validate(created_server)

    def get_server(self, server_id: int) -> Optional[ServerResponse]:
        server = self.server_repo.get_by_id(server_id)
        if not server:
            return None
        return ServerResponse.model_validate(server)

    def get_servers_by_owner(self, owner_id: int) -> List[ServerResponse]:
        servers = self.server_repo.get_by_owner(owner_id)
        return [ServerResponse.model_validate(s) for s in servers]

    def update_server(self, server_id: int, data: ServerUpdate) -> ServerResponse:
        server = self.server_repo.get_by_id(server_id)
        if not server:
            raise ValueError("Сервер не знайдено.")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(server, key, value)

        updated_server = self.server_repo.update(server)
        return ServerResponse.model_validate(updated_server)

    def delete_server(self, server_id: int) -> bool:
        server = self.server_repo.get_by_id(server_id)
        if not server:
            return False
        
        self.server_repo.delete(server_id)
        return True
    
    def mark_online(self, server_id: int):
        server = self.server_repo.get_by_id(server_id)
        if server:
            server.status = "connected"
            server.last_seen = datetime.now(timezone.utc)
            self.server_repo.update(server)

    def cleanup_offline_servers(self, timeout_minutes: int = 5):
        threshold = datetime.now(timezone.utc) - timedelta(minutes=timeout_minutes)
        all_active = self.server_repo.get_all_active() 
        
        for server in all_active:
            if server.last_seen and server.last_seen < threshold:
                server.status = "disconnected"
                self.server_repo.update(server)

    def get_all_active(self) -> List[Server]:
        return self.session.query(Server).filter(Server.status == 'connected').all()