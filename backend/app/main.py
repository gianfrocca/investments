from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.routers import auth, portfolios, assets, transactions, prices, import_data, backup


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    """
    # Startup
    print("🚀 Starting Investment Tracker API...")
    init_db()
    print("✅ Database initialized")

    yield

    # Shutdown
    print("👋 Shutting down Investment Tracker API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-user investment portfolio tracking application",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(portfolios.router)
app.include_router(assets.router)
app.include_router(transactions.router)
app.include_router(prices.router)
app.include_router(import_data.router)
app.include_router(backup.router)


@app.get("/")
def read_root():
    """
    Root endpoint
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}
