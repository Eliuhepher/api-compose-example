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

@app.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    """Create a new client."""
    db_client = models.Client(name=client.name, email=client.email)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    """Get a client by ID."""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@app.get("/clients", response_model=list[schemas.Client])
def read_clients(db: Session = Depends(get_db)):
    """Get all clients."""
    clients = db.query(models.Client).all()
    return clients

@app.put("/clients/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    """ Update a client by ID."""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db_client.email = client.email
    db.commit()
    db.refresh(db_client)
    return db_client

@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Delete a client by ID."""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"detail": "Client deleted"}