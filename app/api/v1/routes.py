from app.api.v1.authentication.auth import router as auth_router
from app.api.v1.authentication.user import router as user_router
# Import other routers here as needed, e.g.:
# from app.api.v1.some_module import router as some_module_router

all_routers = [
    auth_router,
    user_router,
]