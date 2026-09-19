from api.db.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

#Conexion to Aiven redis using render env variable
if settings.REDIS_URI == "":
    raise NotImplementedError("Redis database doesn't exist")

REDIS_URI = settings.REDIS_URI


# Initialize Limiter
limiter = Limiter(key_func= get_remote_address, storage_uri=REDIS_URI)
