from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends

from api.db.session import init_db
from api.events import router as event_router
from fastapi.middleware.cors import CORSMiddleware

from slowapi import  _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from api.limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup up
    init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)

app.include_router(event_router, prefix='/api/events')
#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = False,
    allow_methods = ['GET'],
    allow_headers = ['content-type', 'X-API-KEY']
)


# Register the error handler limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# /api/events
@app.get("/")
@limiter.limit("5/minute")
def read_root(request: Request):
    return {"Hello": "World"}



@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}