import logging
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.dependencies import get_db
from app.schemas.ticket import TicketRead, TicketCreate, TicketUpdate
from app.repositories.tickets import TicketRepository
from sqlalchemy.orm import Session


logger = logging.getLogger("tickets.router")

router = APIRouter()

@router.get("/", response_model=List[TicketRead])
def list_tickets(db: Session = Depends(get_db)) -> list[TicketRead]:
    """Retourne la liste des tickets """
    logger.info("Listing tickets")
    repo = TicketRepository(db)
    items = repo.list_all()
    return items

@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)) -> TicketRead:
    """Crée un ticket et le retourne."""

    repo = TicketRepository(db)
    created = repo.create(payload)
    return created


@router.get("/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> TicketRead:
    """Retourne un ticket, ou une erreur 404 si introuvable."""

    repo = TicketRepository(db)
    obj = repo.get_by_id(ticket_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return obj

@router.put("/{ticket_id}", response_model=TicketRead, status_code=status.HTTP_200_OK)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)) -> TicketRead:
    """Met à jour un ticket, retourne une erreur 404 si introuvable."""

    repo = TicketRepository(db)
    updated = repo.update_full(ticket_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return updated


@router.patch("/{ticket_id}/close", response_model=TicketRead)
def close_ticket(ticket_id: int, db: Session = Depends(get_db)) -> TicketRead:
    """Ferme un ticket, retourne une erreur 404 si introuvable,
    ou une erreur 400 si le ticket est déjà fermé."""

    repo = TicketRepository(db)
    closed = repo.close(ticket_id)
    if closed is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if closed == "already_closed":
        raise HTTPException(status_code=400, detail="Ticket is already closed")
    return closed
