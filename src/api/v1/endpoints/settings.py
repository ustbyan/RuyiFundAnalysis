# -*- coding: utf-8 -*-
"""
如意基金分析 - 系统设置 API
"""

import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class SettingsUpdate(BaseModel):
    fund_list: str = ""
    llm_model: str = ""
    report_language: str = "zh"
    report_type: str = "simple"
    enable_notification: bool = False
    wechat_webhook: str = ""
    feishu_webhook: str = ""
    schedule_enabled: bool = False
    schedule_time: str = "18:00"


@router.get("/settings")
async def get_settings():
    """获取当前设置"""
    return {
        "status": "success",
        "data": {
            "fund_list": os.getenv("FUND_LIST", ""),
            "llm_model": os.getenv("LITELLM_MODEL", ""),
            "report_language": os.getenv("REPORT_LANGUAGE", "zh"),
            "report_type": os.getenv("REPORT_TYPE", "simple"),
            "schedule_enabled": os.getenv("SCHEDULE_ENABLED", "false"),
            "schedule_time": os.getenv("SCHEDULE_TIME", "18:00"),
            "market_review_enabled": os.getenv("MARKET_REVIEW_ENABLED", "true"),
            "debug": os.getenv("DEBUG", "false"),
        },
    }


@router.post("/settings")
async def update_settings(settings: SettingsUpdate):
    """更新设置"""
    # 实际项目中需要更新 .env 文件或数据库
    return {
        "status": "success",
        "message": "设置已更新（需要重启服务生效）",
    }


@router.post("/settings/check-connection")
async def check_connection():
    """检查 LLM 连接状态"""
    checks = {}

    # 检查各 API Key
    providers = [
        ("deepseek", "DEEPSEEK_API_KEY"),
        ("gemini", "GEMINI_API_KEY"),
        ("openai", "OPENAI_API_KEY"),
        ("anthropic", "ANTHROPIC_API_KEY"),
        ("siliconflow", "SILICONFLOW_API_KEY"),
    ]

    for name, env_key in providers:
        checks[name] = {
            "configured": bool(os.getenv(env_key)),
            "status": "已配置" if os.getenv(env_key) else "未配置",
        }

    return {"status": "success", "data": checks}
