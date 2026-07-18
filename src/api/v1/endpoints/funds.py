# -*- coding: utf-8 -*-
"""
如意基金分析 - 基金查询 API
"""

from fastapi import APIRouter, HTTPException, Query

from src.data.fund_data import search_funds, fetch_fund_data, fetch_market_index

router = APIRouter()


@router.get("/funds/search")
async def search(keyword: str = Query(..., min_length=1, description="搜索关键词")):
    """搜索基金"""
    try:
        results = search_funds(keyword)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/funds/{fund_code}/info")
async def fund_info(fund_code: str):
    """获取基金基本信息"""
    try:
        data = fetch_fund_data(fund_code)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/funds/{fund_code}/nav")
async def fund_nav(fund_code: str):
    """获取基金净值数据"""
    try:
        data = fetch_fund_data(fund_code)
        nav = data.get("nav_data")
        if nav is not None and hasattr(nav, "to_dict"):
            nav_data = nav.to_dict(orient="records")
        else:
            nav_data = []
        return {"status": "success", "data": nav_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/indices")
async def market_indices():
    """获取市场指数"""
    try:
        indices = fetch_market_index()
        return {"status": "success", "data": indices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
