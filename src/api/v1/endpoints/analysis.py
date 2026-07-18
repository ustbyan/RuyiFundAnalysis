# -*- coding: utf-8 -*-
"""
如意基金分析 - 分析 API
"""

import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from src.data.fund_data import fetch_fund_data
from src.analysis.fund_analyzer import analyze_fund
from src.analysis.market_review import review_market
from src.data.storage import get_analysis_history, save_analysis

router = APIRouter()


@router.post("/analyze/{fund_code}")
async def analyze_single_fund(fund_code: str):
    """分析单只基金"""
    try:
        config = {}  # 简化配置
        fund_data = fetch_fund_data(fund_code)

        if not fund_data.get("basic_info"):
            raise HTTPException(status_code=404, detail=f"未找到基金 {fund_code} 的数据")

        analysis_id = str(uuid.uuid4())[:8]
        result = analyze_fund(fund_code, fund_data, config)
        save_analysis(analysis_id, fund_code, result)

        return {"status": "success", "data": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/history")
async def analysis_history(fund_code: str = None, limit: int = 20):
    """获取分析历史"""
    try:
        history = get_analysis_history(fund_code, limit)
        return {"status": "success", "data": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market-review")
async def market_review():
    """获取大盘复盘"""
    try:
        result = review_market({})
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/batch")
async def batch_analyze(fund_codes: list[str]):
    """批量分析基金"""
    results = []
    config = {}

    for code in fund_codes:
        try:
            fund_data = fetch_fund_data(code)
            if fund_data.get("basic_info"):
                analysis_id = str(uuid.uuid4())[:8]
                result = analyze_fund(code, fund_data, config)
                save_analysis(analysis_id, code, result)
                results.append({"code": code, "status": "success", "data": result})
            else:
                results.append({"code": code, "status": "not_found"})
        except Exception as e:
            results.append({"code": code, "status": "error", "error": str(e)})

    return {"status": "success", "data": results}
