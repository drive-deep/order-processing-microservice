from fastapi import APIRouter
from app.services.metrics_service import get_metrics

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/")
async def metrics_api():
    """Retrieve order processing metrics."""
    return await get_metrics()
