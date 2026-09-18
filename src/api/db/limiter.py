from slowapi.storage import RedisStorage
from .config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

#Conexion to Aiven redis using render env variable
if settins.DATABASE_REDIS == "":
    raise NotImplementedError("Redis database doesn't exist")

REDIS_URI = settings.DATABASE_REDIS
redis_storage = RedisStorage(REDIS_URI)

# Initialize Limiter
limiter = Limiter(key_func= get_remote_address, storage=redis_storage)