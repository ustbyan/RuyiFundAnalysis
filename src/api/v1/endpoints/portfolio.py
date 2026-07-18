# -*- coding: utf-8 -*-
"""
如意基金分析 - 持仓管理 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.data.storage import get_portfolio, update_portfolio

router = APIRouter()


class PortfolioItem(BaseModel):
    fund_code: str
    fund_name: str = ""
    shares: float = 0
    cost_price: float = 0
    account_name: str = "默认账户"


@router.get("/portfolio")
async def list_portfolio(account: str = "默认账户"):
    """获取持仓列表"""
    try:
        items = get_portfolio(account)
        return {"status": "success", "data": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio")
async def add_portfolio_item(item: PortfolioItem):
    """添加/更新持仓"""
    try:
        update_portfolio(
            fund_code=item.fund_code,
            fund_name=item.fund_name,
            shares=item.shares,
            cost_price=item.cost_price,
            account_name=item.account_name,
        )
        return {"status": "success", "message": f"已更新 {item.fund_code} 持仓"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio/summary")
async def portfolio_summary(account: str = "默认账户"):
    """持仓汇总"""
    try:
        items = get_portfolio(account)
        total_value = sum(item.get("market_value", 0) for item in items)
        total_profit = sum(item.get("profit_loss", 0) for item in items)

        return {
            "status": "success",
            "data": {
                "total_value": total_value,
                "total_profit": total_profit,
                "item_count": len(items),
                "items": items,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
