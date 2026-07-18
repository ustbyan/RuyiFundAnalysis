# -*- coding: utf-8 -*-
"""
如意基金分析 - 通知模块
支持企业微信、飞书、钉钉、Telegram、邮件等多种渠道
"""

import json
import logging
import os
from datetime import datetime

import requests

logger = logging.getLogger(__name__)


def send_analysis_notification(results: list, config: dict):
    """
    发送分析结果通知
    
    支持多渠道：企业微信、飞书、钉钉、Telegram、邮件
    """
    # 构建消息内容
    message = _build_notification_message(results)

    # 企业微信
    wechat_webhook = os.getenv("WECHAT_WEBHOOK_URL")
    if wechat_webhook:
        try:
            _send_wechat(wechat_webhook, message)
        except Exception as e:
            logger.warning(f"企业微信通知失败: {e}")

    # 飞书
    feishu_webhook = os.getenv("FEISHU_WEBHOOK_URL")
    if feishu_webhook:
        try:
            _send_feishu(feishu_webhook, message)
        except Exception as e:
            logger.warning(f"飞书通知失败: {e}")

    # 钉钉
    dingtalk_webhook = os.getenv("DINGTALK_WEBHOOK_URL")
    if dingtalk_webhook:
        try:
            _send_dingtalk(dingtalk_webhook, message)
        except Exception as e:
            logger.warning(f"钉钉通知失败: {e}")

    # Telegram
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if telegram_token and telegram_chat_id:
        try:
            _send_telegram(telegram_token, telegram_chat_id, message)
        except Exception as e:
            logger.warning(f"Telegram通知失败: {e}")

    # 邮件
    email_sender = os.getenv("EMAIL_SENDER")
    email_password = os.getenv("EMAIL_PASSWORD")
    if email_sender and email_password:
        try:
            _send_email(email_sender, email_password, message, config)
        except Exception as e:
            logger.warning(f"邮件通知失败: {e}")


def _build_notification_message(results: list) -> str:
    """构建通知消息"""
    today = datetime.now().strftime("%Y-%m-%d")

    parts = [f"📊 如意基金分析日报 ({today})", ""]

    fund_results = [r for r in results if r.get("type") == "fund_analysis"]
    for i, fr in enumerate(fund_results):
        code = fr.get("code", "")
        data = fr.get("data", {})
        analysis = data.get("analysis", {}) if isinstance(data, dict) else {}

        parts.append(f"【{i+1}】{code} {analysis.get('fund_name', code)}")
        parts.append(f"  评级: {analysis.get('rating', 'N/A')}")
        parts.append(f"  综合评分: {analysis.get('overall_score', 'N/A')}/100")
        parts.append(f"  摘要: {analysis.get('summary', '')}")
        parts.append(f"  建议: {analysis.get('advice', {}).get('target_action', '') if isinstance(analysis.get('advice'), dict) else ''}")
        parts.append("")

    # 汇总
    summary = [r for r in results if r.get("type") == "summary"]
    if summary:
        s = summary[0].get("data", {})
        parts.append(f"📈 分析汇总: 共 {s.get('total', 0)} 只，成功 {s.get('success', 0)} 只")

    # 大盘复盘
    market = [r for r in results if r.get("type") == "market_review"]
    if market:
        m = market[0].get("data", {})
        if m.get("summary"):
            parts.append(f"🌍 大盘环境: {m.get('summary', '')}")

    parts.append("")
    parts.append("---")
    parts.append("由 如意基金分析 RuyiFundAnalysis 自动生成")

    return "\n".join(parts)


def _send_wechat(webhook_url: str, message: str):
    """企业微信通知"""
    data = {
        "msgtype": "markdown",
        "markdown": {"content": message},
    }
    resp = requests.post(webhook_url, json=data, timeout=10)
    resp.raise_for_status()


def _send_feishu(webhook_url: str, message: str):
    """飞书通知"""
    data = {
        "msg_type": "text",
        "content": {"text": message},
    }
    resp = requests.post(webhook_url, json=data, timeout=10)
    resp.raise_for_status()


def _send_dingtalk(webhook_url: str, message: str):
    """钉钉通知"""
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "如意基金分析日报",
            "text": message,
        },
    }
    resp = requests.post(webhook_url, json=data, timeout=10)
    resp.raise_for_status()


def _send_telegram(token: str, chat_id: str, message: str):
    """Telegram 通知"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    resp = requests.post(url, json=data, timeout=10)
    resp.raise_for_status()


def _send_email(sender: str, password: str, message: str, config: dict):
    """邮件通知（简化版）"""
    # 这里需要完整的 SMTP 实现
    # 目前作为框架占位
    logger.info(f"[邮件] 准备发送通知到 {sender}")
    # 实际发送逻辑：
    # import smtplib
    # from email.mime.text import MIMEText
    # msg = MIMEText(message, "plain", "utf-8")
    # ...
