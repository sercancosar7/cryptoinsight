from fastapi import APIRouter, HTTPException, Query

from app.services.alert_service import AlertService, AlertCreate, Alert

router = APIRouter()
alert_service = AlertService()


@router.post("", response_model=Alert, status_code=201)
async def create_alert(data: AlertCreate):
    try:
        return alert_service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=list[Alert])
async def get_user_alerts(
    user_id: str,
    active_only: bool = Query(default=True),
):
    """Get all price alerts for a user. Defaults to active alerts only."""
    alerts = alert_service.get_by_user(user_id, active_only=active_only)
    return alerts


@router.delete("/{user_id}/{alert_id}", status_code=204)
async def delete_alert(user_id: str, alert_id: str):
    deleted = alert_service.delete(user_id, alert_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert not found")
