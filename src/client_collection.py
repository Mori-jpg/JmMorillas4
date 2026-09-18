from typing import List, Optional
try:
    from .client import Client
except ImportError:
    from client import Client

class ClientCollection:
    def __init__(self, clients: List[Client]):
        self.clients = clients

    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        for c in self.clients:
            if c.client_id == client_id:
                return c
        return None

    def clients_by_country(self, country: str) -> List[Client]:
        # OBLIGATORIO: bucle + condicional
        result = []
        for c in self.clients:
            if c.country.lower() == country.lower():
                result.append(c)
        return result
