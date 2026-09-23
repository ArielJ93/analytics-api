from typing import List, Annotated
from pydantic import StringConstraints
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select, func
from sqlalchemy import text, cast
from sqlalchemy.dialects.postgresql import INTERVAL
from datetime import datetime, timedelta, timezone
from api.db.session import get_session
from api.db.config import settings

from .models import (
    EventModel, 
    EventBucketSchema, 
    EventCreateSchema,
    DurationEnum,
    HistoryEnum, 
    EventCreateResponse
)

from api.limiter import limiter
from fastapi.security import APIKeyHeader
from api.dependencies import streamlit_api_key as sta, automation_api_key as apk

router = APIRouter()

# DEFAULT_SYMBOLS = [
#         "btc", "eth", "ltc", "bch", "bnb", "eos", "xrp", "xlm", "link", "dot", "yfi", "sol",
#     ]

# Get data here
# List View

@router.get("", response_model=List[EventBucketSchema])
@limiter.limit("20/minute")
def get_crypto_metrics(
    request: Request,
    symbol: 
        Annotated[
            List[
                Annotated[
                    str,
                    StringConstraints(max_length=12, pattern=r"^[a-zA-Z0-9_]+$")
                ]
            ],
            Query(..., 
                max_length=120, 
                description=   
                    """**Top 100 Coingecko cryptos**
                    
Enter valid market symbols (e.g., `btc`, `eth`, `sol`).
You can add multiple items to compare""",
                openapi_examples={
                    "Example 1": {
                        "summary": "Example with Bitcoin",
                        "value": ["btc"]
                        },
                    "Example 2": {
                        "summary": "Multiple coins",
                        "value": ["eth", "sol", "ada", "usdt", "usdc"]
                        }
                    })
        ],
    history: HistoryEnum = HistoryEnum.seven_days,
    duration: DurationEnum = DurationEnum.one_hour,
    session:Session=Depends(get_session),
    ):
    
    
    duration_interval = cast(duration, INTERVAL)
    history_interval = cast(history, INTERVAL)
    #Round timestamp down into fixed intervals based on the duration parameter
    bucket = func.public.time_bucket(duration_interval, EventModel.timestamp)
    
    lookup_symbols = symbol if isinstance(symbol,list) and len(symbol) > 0 else None
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
                EventModel.symbol.in_(lookup_symbols),
                EventModel.timestamp >= func.now() - history_interval
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
@router.post("", response_model=EventCreateResponse, dependencies=[Depends(apk)])
@limiter.limit("5/minute")
def insert_crypto_data(
        request: Request,
        payload: List[EventCreateSchema], 
        session: Session = Depends(get_session),
        ):

    data = [EventModel.model_validate(i.model_dump()) for i in payload]
    
    session.add_all(data)
    session.commit()
    
    return {"status": "success", "inserted_records": len(data)}


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