# -*- coding: utf-8 -*-
"""
如意基金分析 - LLM 用量监控 API
"""

from fastapi import APIRouter, HTTPException

from src.data.storage import get_llm_usage_summary

router = APIRouter()


@router.get("/usage/llm")
async def llm_usage(period: str = "today"):
    """获取 LLM Token 用量"""
    try:
        summary = get_llm_usage_summary(period)
        total_tokens = sum(item.get("total_tokens", 0) for item in summary)

        return {
            "status": "success",
            "data": {
                "period": period,
                "total_tokens": total_tokens,
                "details": summary,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
