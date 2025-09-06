from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, user, chart, chat, daily
from app.core.config import settings
from app.core.middleware import ErrorHandlingMiddleware
from app.database import connect_to_mongodb, close_mongodb_connection
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Astrology Backend API",
    description="Backend API for the astrology application",
    version="1.0.0"
)

# Add middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_CORS_ORIGINS + ["https://cosmic-insights-ai-tmdlw.web.app","http://localhost:9002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/user", tags=["user"])
# Add additional route for account management for backward compatibility
app.include_router(user.router, prefix="/api/v1", tags=["user"], include_in_schema=False)
app.include_router(chart.router, prefix="/api/v1/chart", tags=["chart"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(daily.router, prefix="/api/v1/daily", tags=["daily"])

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup."""
    logger.info("Connecting to MongoDB...")
    connect_to_mongodb()
    logger.info("Connected to MongoDB successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown."""
    logger.info("Closing MongoDB connection...")
    close_mongodb_connection()
    logger.info("MongoDB connection closed")

@app.get("/")
async def root():
    return {"message": "Welcome to the Astrology Backend API"}
