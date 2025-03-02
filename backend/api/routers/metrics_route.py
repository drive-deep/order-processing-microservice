from fastapi import APIRouter
from backend.api.services.metrics_service import get_metrics

router = APIRouter()

@router.get("/")
async def metrics_api():
    """Retrieve order processing metrics."""
    return await get_metrics()
