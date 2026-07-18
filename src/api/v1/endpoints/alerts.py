# -*- coding: utf-8 -*-
"""
如意基金分析 - 告警 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# 内存告警存储（实际应使用数据库）
_alerts_store = []


class AlertCreate(BaseModel):
    fund_code: str
    alert_type: str  # price_cross, change_percent, volume_spike
    threshold: float
    direction: str = "above"  # above/below/up/down


@router.get("/alerts")
async def list_alerts():
    """获取告警列表"""
    return {"status": "success", "data": _alerts_store}


@router.post("/alerts")
async def create_alert(alert: AlertCreate):
    """创建告警"""
    alert_data = alert.model_dump()
    alert_data["id"] = len(_alerts_store) + 1
    alert_data["enabled"] = True
    _alerts_store.append(alert_data)
    return {"status": "success", "data": alert_data}


@router.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: int):
    """删除告警"""
    global _alerts_store
    _alerts_store = [a for a in _alerts_store if a["id"] != alert_id]
    return {"status": "success", "message": f"告警 {alert_id} 已删除"}
