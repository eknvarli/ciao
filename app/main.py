from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler, Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.api.router import api_router
from app.core.cache import init_redis, close_redis

def create_app() -> FastAPI:
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url=None,
    )
    app.state.limiter = limiter

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred.",
                    "details": str(exc)
                }
            }
        )
        
    @app.on_event("startup")
    async def startup_event():
        await init_redis()
        from app.db.session import engine, Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    @app.on_event("shutdown")
    async def shutdown_event():
        await close_redis()

    return app

app = create_app()
