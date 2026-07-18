# -*- coding: utf-8 -*-
"""
如意基金分析 - 自选基金管理 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.data.storage import get_watchlist, add_to_watchlist, remove_from_watchlist

router = APIRouter()


class WatchlistItem(BaseModel):
    fund_code: str
    fund_name: str = ""
    fund_type: str = ""
    group_name: str = "默认"


@router.get("/watchlist")
async def list_watchlist():
    """获取自选列表"""
    try:
        items = get_watchlist()
        return {"status": "success", "data": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/watchlist")
async def add_watchlist_item(item: WatchlistItem):
    """添加自选基金"""
    try:
        add_to_watchlist(
            fund_code=item.fund_code,
            fund_name=item.fund_name,
            fund_type=item.fund_type,
            group_name=item.group_name,
        )
        return {"status": "success", "message": f"已添加 {item.fund_code}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/watchlist/{fund_code}")
async def delete_watchlist_item(fund_code: str):
    """移除自选基金"""
    try:
        remove_from_watchlist(fund_code)
        return {"status": "success", "message": f"已移除 {fund_code}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
