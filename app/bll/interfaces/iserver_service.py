from abc import ABC, abstractmethod

class IServerService(ABC):
    @abstractmethod
    def create_server(self, owner_id: int, ip_address: str, name: str):
        pass

    @abstractmethod
    def get_server(self, server_id: int):
        pass

    @abstractmethod
    def get_servers_by_owner(self, owner_id: int):
        pass

    @abstractmethod
    def update_server(self, server_id: int, data: dict):
        pass

    @abstractmethod
    def delete_server(self, server_id: int):
        pass
