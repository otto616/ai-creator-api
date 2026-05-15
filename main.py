from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai_endpoints
from limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler # ignore type

# Init API with some metadata
app = FastAPI(
    title="AI Creator API",
    description="API for processing and generating text for content creators",
    version="1.0.0",
)

# Register the limiter in the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS config.
app.add_middleware(
    CORSMiddleware, #ignore type
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_endpoints.router, prefix="/api/ai", tags=["Artificial Intelligence"])