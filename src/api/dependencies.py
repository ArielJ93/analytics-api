from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from api.db.config import settings


header_scheme = APIKeyHeader(name="X-API-KEY")

def streamlit_api_key(key: str=Depends(header_scheme)):
    if key == settings.STREAMLIT_API_KEY:
        return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
    
    

def automation_api_key(key: str=Depends(header_scheme)):
    if key == settings.AUTOMATION_API_KEY:
        return key

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
