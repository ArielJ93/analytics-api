import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy import text, cast
from sqlalchemy.dialects.postgresql import INTERVAL
from datetime import datetime, timedelta, timezone
from api.db.session import get_session
from api.db.config import settings
#from timescaledb.hyperfunctions import time_bucket

from .models import (
    EventModel, 
    EventBucketSchema, 
    EventCreateSchema,
    # get_utc_now,
    # EventListSchema,
    #EventUpdateSchema
)
router = APIRouter()

DEFAULT_SYMBOLS = [
        "btc", "eth", "ltc", "bch", "bnb", "eos", "xrp", "xlm", "link", "dot", "yfi", "sol",
    ]

# Get data here
# List View
# GET /api/events/
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str=Query(default='1 day'),
    symbol: List[str]=Query(default=None),
    session:Session=Depends(get_session)):
    
    
    interval = cast(duration, INTERVAL)
    bucket = func.public.time_bucket(interval, EventModel.timestamp)
    lookup_symbols = symbol if isinstance(symbol,list) and len(symbol) > 0 else DEFAULT_SYMBOLS
    query = (
        select(
            EventModel.symbol,
            bucket.label("bucket"),
            func.avg(EventModel.price).label("avg_price"),
            func.count().label("count"),
            func.last(EventModel.market_cap, EventModel.timestamp).label("market_cap"),
            func.last(EventModel.volume_24h, EventModel.timestamp).label("volume_24h"),
            func.last(EventModel.change_24h, EventModel.timestamp).label("change_24h")
                )
            .where(
                EventModel.symbol.in_(lookup_symbols)
                )
            .group_by(
                bucket, 
                EventModel.symbol
                )
            .order_by(bucket)
        )
    results = session.exec(query).fetchall()
    return results

# SEND DATA HERE
# create view
# POST /api/events/
@router.post("/", response_model=List[EventModel])
def create_event(
        payload: List[EventCreateSchema], 
        session: Session = Depends(get_session)):

    data = [EventModel.model_validate(i.model_dump()) for i in payload]
    
    session.add_all(data)
    session.commit()
    for i in data:
        session.refresh(i)
    
    return data


# GET /api/events/12
# @router.get("/{event_id}", response_model=EventModel)
# def get_event(event_id:int, session: Session = Depends(get_session)):
#     # a single row
#     query = select(EventModel).where(EventModel.id == event_id)
#     result = session.exec(query).first()
#     if not result:
#         raise HTTPException(status_code=404, detail="Event not found")
#     return result


# @router.put("/{event_id}", response_model=EventModel)
# def update_event(
#     event_id: int, 
#     payload:EventUpdateSchema, 
#     session:Session=Depends(get_session)):
    
#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Event not found")
#     data = payload.model_dump()
#     for k, v in data.items():
#         setattr(obj, k, v)
#     session.add(obj)
#     session.commit()
#     session.refresh(obj)
#     return obj

# @router.delete("/{event_id}", response_model=EventModel)
# def delete_event(event_id: int, session:Session=Depends(get_session)):
#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Event not found")
#     session.delete(obj)
#     session.commit()

#     return obj