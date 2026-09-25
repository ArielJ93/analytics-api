from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import DateTime, Column, Integer, BigInteger

from sqlmodel import SQLModel, Field
from enum import Enum

# page visits at any given time

def get_utc_now():
    return datetime.now(timezone.utc)

class EventModel(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        sa_column= Column(Integer, autoincrement=True, primary_key=True) 
        )
    #description: Optional[str] = ""
    timestamp: datetime = Field(
        default_factory= get_utc_now,
        sa_column=Column(DateTime(timezone=True), primary_key=True, nullable=False),
    )
    
    symbol: Optional[str] = Field(default="", index=True)
    price: Optional[float] = Field(default=0.0)
    volume_24h: Optional[float] = Field(default=0.0)   #float64            
    change_24h: Optional[float] = Field(default=0.0)   #float64            
    market_cap: Optional[int] = Field(sa_column= Column(BigInteger), default=0)   #int64              
    rank: Optional[int] = Field(default=0)  #int64              
    high_24h: Optional[float] = Field(default=0.0)  #float64            
    low_24h: Optional[float] = Field(default=0.0)   #float64 

    #__chunk_time_interval__ = "INTERVAL 1 day"
    #__drop_after__ = "INTERVAL 3 months"

    #update_at: datetime = Field(
    #    default_factory = get_utc_now,
    #    sa_type= DateTime(timezone=True),
    #    sa_column_kwargs = {"onupdate": get_utc_now},
    #    nullable=False
    #)

class EventCreateSchema(SQLModel):
    symbol: str = Field(max_length=10)
    price: float = Field(ge=0.0, le=10000000000000.0)
    volume_24h: Optional[float] = Field(default=0.0, ge=0.0, le=10000000000000.0)   #float64            
    change_24h: Optional[float] = Field(default=0.0, ge=-100000.0, le=100000.0)   #float64            
    market_cap: Optional[int] = Field(default=0,  ge=0, le=100000000000000)   #int64              
    rank: Optional[int] = Field(default=0, ge=0, le=100000)  #int64              
    high_24h: Optional[float] = Field(default=0.0, ge=0.0, le=10000000000000.0)  #float64            
    low_24h: Optional[float] = Field(default=0.0, ge=0.0, le=10000000000000.0)   #float64 

class EventCreateResponse(SQLModel):
    status: str
    inserted_records: int
# class EventUpdateSchema(SQLModel):
#     description: str


# {"id": 12}

# class EventListSchema(SQLModel):
#     results: List[EventModel]
#     count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    symbol: str
    avg_price: Optional[float] = 0.0
    count: int
    market_cap: int
    volume_24h: Optional[float] = 0.0            
    change_24h: Optional[float] =  0.0   
    
    
    
class DurationEnum(str, Enum): 
    fifteen_min = "15 minutes" 
    one_hour = "1 hour"
    four_hour = '4 hours'
    one_day = "1 day"
    


class HistoryEnum(str, Enum):
    one_day = "1 day"
    seven_days = "7 days"
    thirty_days = "30 days"
    