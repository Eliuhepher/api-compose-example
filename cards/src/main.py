from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    """Create a new session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cards", response_model=schemas.Card)
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    """Create a new card."""
    db_client = models.Card(issuer=card.issuer, card_number=card.card_number, type=card.type, status=card.status, cardholder_id=card.cardholder_id, expiration_date=card.expiration_date)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/cards/{card_id}", response_model=schemas.Card)
def read_card(card_id: int, db: Session = Depends(get_db)):
    """Get a card by ID."""
    db_client = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_client

@app.get("/cards", response_model=list[schemas.Card])
def read_cards(db: Session = Depends(get_db)):
    """Get all Cards."""
    cards = db.query(models.Card).all()
    return cards

@app.put("/cards/{card_id}", response_model=schemas.Card)
def update_card(card_id: int, client: schemas.CardUpdate, db: Session = Depends(get_db)):
    """ Update a card by ID."""
    db_client = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db_client.email = client.email
    db.commit()
    db.refresh(db_client)
    return db_client

@app.delete("/cards/{card_id}")
def delete_client(card_id: int, db: Session = Depends(get_db)):
    """Delete a card by ID."""
    db_client = db.query(models.Card).filter(models.Card.id == card_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Card not found")
    db.delete(db_client)
    db.commit()
    return {"detail": "Card deleted"}