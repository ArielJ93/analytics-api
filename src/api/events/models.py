from datetime import datetime, timezone
from typing import List, Optional
# from pydantic import BaseModel, Field
#import sqlmodel
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime, Column, Integer
#from timescaledb import TimescaleModel
#from timescaledb.utils import get_utc_now

# page visits at any given time

def get_utc_now():
    return datetime.now(timezone.utc)

class EventModel(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        sa_column= Column(Integer, autoincrement=True, primary_key=True) 
        )
    #description: Optional[str] = ""
    created_at: datetime = Field(
        default_factory= get_utc_now,
        sa_column=Column(DateTime(timezone=True), primary_key=True, nullable=False),
    )
    
    page: str = Field(index=True) # /about, /contact, # pricing
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 

    #__chunk_time_interval__ = "INTERVAL 1 day"
    #__drop_after__ = "INTERVAL 3 months"

    #update_at: datetime = Field(
    #    default_factory = get_utc_now,
    #    sa_type= DateTime(timezone=True),
    #    sa_column_kwargs = {"onupdate": get_utc_now},
    #    nullable=False
    #)

class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True) # browser
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True) 
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0) 


# class EventUpdateSchema(SQLModel):
#     description: str


# {"id": 12}

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int