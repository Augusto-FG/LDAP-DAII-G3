from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer
import structlog
from app.api.v1.routes import all_routers
from app.config.settings import settings
from app.config.ldap_singleton import get_ldap_port_instance
from app.utils.logging import configure_logging


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

configure_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application ...")
    ldap_instance = await get_ldap_port_instance()
    yield
    # Cleanup LDAP connection on shutdown
    if hasattr(ldap_instance, "conn") and ldap_instance.conn.bound:
        ldap_instance.conn.unbind()
        logger.info("LDAP connection purged on shutdown.")
    
app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)


for router in all_routers:
    app.include_router(router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "FastAPI OpenLDAP AD Service"}

