from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketStatus

class TicketRepository:
    """Accès données pour les tickets"""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> List[Ticket]:
        """Retourne tous les tickets."""
        return self.db.query(Ticket).all()

    def create(self, payload: TicketCreate) -> Ticket:
        """Crée un ticket et le retourne (avec id + created_at remplis)."""
        obj = Ticket(
            title=payload.title,
            description=payload.description,
            # status par défaut = "open" via le modèle
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_by_id(self, ticket_id:int)-> Optional[Ticket]:
        item = self.db.get(Ticket, ticket_id)

        return item

    def update_full(self, ticket_id: int, payload: TicketUpdate) -> Optional[Ticket]:
        """Met à jour entièrement (title, description). Retourne None si introuvable."""
        obj = self.db.get(Ticket, ticket_id)
        if obj is None:
            return None
        obj.title = payload.title
        obj.description = payload.description
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def close(self, ticket_id: int) -> Optional[Ticket]:
        """Ferme un ticket. 
        - Retourne None si introuvable.
        - Retourne 'already_closed' si le ticket est déjà fermé.
        - Sinon, ferme et retourne l'objet.
        """
        obj = self.db.get(Ticket, ticket_id)
        if obj is None:
            return None
        if obj.status == TicketStatus.CLOSED:
            return "already_closed"
        obj.status = TicketStatus.CLOSED
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

