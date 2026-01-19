from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import database, crud, schemas

app = FastAPI(title="Telegram Analytics API")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint 1: Top Products
@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

# Endpoint 2: Channel Activity
@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel_name)

# Endpoint 3: Message Search
@app.get("/api/search/messages", response_model=List[schemas.MessageSearchResult])
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    return crud.search_messages(db, query, limit)

# Endpoint 4: Visual Content Stats
@app.get("/api/reports/visual-content", response_model=List[schemas.VisualContentStat])
def visual_content(db: Session = Depends(get_db)):
    return crud.get_visual_content_stats(db)
