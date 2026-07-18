# -*- coding: utf-8 -*-
"""
如意基金分析 - 全局配置管理
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class LLMConfig(BaseModel):
    """LLM 模型配置"""
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7


class DataSourceConfig(BaseModel):
    """数据源配置"""
    efinance_priority: int = 0
    akshare_priority: int = 1
    tushare_priority: int = 2
    tushare_token: Optional[str] = None


class NotifyConfig(BaseModel):
    """通知配置"""
    wechat_webhook: Optional[str] = None
    feishu_webhook: Optional[str] = None
    dingtalk_webhook: Optional[str] = None
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    email_sender: Optional[str] = None
    email_password: Optional[str] = None


class AppConfig:
    """应用全局配置"""

    def __init__(self):
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_dir = Path(os.getenv("LOG_DIR", "./logs"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.database_path = os.getenv("DATABASE_PATH", "./data/fund_analysis.db")
        self.max_workers = int(os.getenv("MAX_WORKERS", "3"))
        self.report_language = os.getenv("REPORT_LANGUAGE", "zh")
        self.report_type = os.getenv("REPORT_TYPE", "simple")

        # LLM 配置
        self.llm = LLMConfig(
            model=os.getenv("LITELLM_MODEL", ""),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        )

        # 数据源配置
        self.data = DataSourceConfig(
            tushare_token=os.getenv("TUSHARE_TOKEN"),
        )

        # 通知配置
        self.notify = NotifyConfig(
            wechat_webhook=os.getenv("WECHAT_WEBHOOK_URL"),
            feishu_webhook=os.getenv("FEISHU_WEBHOOK_URL"),
            dingtalk_webhook=os.getenv("DINGTALK_WEBHOOK_URL"),
            telegram_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            email_sender=os.getenv("EMAIL_SENDER"),
            email_password=os.getenv("EMAIL_PASSWORD"),
        )

        # Web 配置
        self.webui_host = os.getenv("WEBUI_HOST", "127.0.0.1")
        self.webui_port = int(os.getenv("WEBUI_PORT", "8000"))
        self.webui_enabled = os.getenv("WEBUI_ENABLED", "false").lower() == "true"
        self.admin_auth_enabled = os.getenv("ADMIN_AUTH_ENABLED", "false").lower() == "true"

    def get_fund_list(self) -> list:
        """获取自选基金列表"""
        fund_str = os.getenv("FUND_LIST", "")
        if not fund_str:
            return []
        return [f.strip() for f in fund_str.split(",") if f.strip()]


# 全局单例
config = AppConfig()
