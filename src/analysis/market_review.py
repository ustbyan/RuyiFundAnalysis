# -*- coding: utf-8 -*-
"""
如意基金分析 - 大盘复盘模块
分析市场指数环境，为基金分析提供宏观背景
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def review_market(config: dict) -> dict:
    """
    市场大盘复盘
    
    分析主要指数的走势、板块轮动、市场情绪等宏观因素
    """
    try:
        from src.data.fund_data import fetch_market_index

        indices = fetch_market_index()

        if not indices:
            return {
                "status": "warning",
                "summary": "无法获取市场指数数据",
                "timestamp": datetime.now().isoformat(),
            }

        # 分析各指数
        index_analysis = {}
        total_change = 0
        up_count = 0
        down_count = 0

        for name, data in indices.items():
            change_pct = data.get("change_pct", 0)
            total_change += change_pct
            if change_pct > 0:
                up_count += 1
            elif change_pct < 0:
                down_count += 1

            index_analysis[name] = {
                "close": data.get("close"),
                "change_pct": round(change_pct, 2),
                "trend": "上涨" if change_pct > 0 else "下跌" if change_pct < 0 else "平盘",
            }

        # 市场情绪判断
        avg_change = total_change / len(indices) if indices else 0
        if avg_change > 1:
            sentiment = "乐观"
            sentiment_advice = "市场情绪积极，可适当增加权益类基金配置"
        elif avg_change > 0:
            sentiment = "平稳偏多"
            sentiment_advice = "市场整体平稳，维持原有配置"
        elif avg_change > -1:
            sentiment = "平稳偏空"
            sentiment_advice = "市场小幅调整，关注回调买入机会"
        else:
            sentiment = "谨慎"
            sentiment_advice = "市场情绪低迷，建议增加固收类基金比例"

        summary = f"市场情绪: {sentiment}。{up_count}涨{down_count}跌，平均涨跌幅 {avg_change:.2f}%"
        if sentiment_advice:
            summary += f"。{sentiment_advice}"

        return {
            "status": "success",
            "summary": summary,
            "sentiment": sentiment,
            "avg_change_pct": round(avg_change, 2),
            "up_count": up_count,
            "down_count": down_count,
            "indices": index_analysis,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"大盘复盘失败: {e}")
        return {
            "status": "error",
            "summary": f"大盘复盘失败: {str(e)}",
            "timestamp": datetime.now().isoformat(),
        }
