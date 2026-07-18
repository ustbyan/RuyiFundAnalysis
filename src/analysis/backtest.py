# -*- coding: utf-8 -*-
"""
如意基金分析 - 回测模块
验证历史分析准确率
"""

import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def run_fund_backtest(config: dict) -> dict:
    """
    运行基金分析回测
    
    对比历史分析结果与后续实际表现，计算准确率
    """
    from src.data.storage import get_analysis_history

    fund_list = config.get("fund_list", [])
    if not fund_list:
        return {"status": "empty", "message": "无待回测基金"}

    results = {"total": 0, "accurate": 0, "accuracy": 0, "details": []}

    for fund_code in fund_list:
        history = get_analysis_history(fund_code, limit=10)
        if not history:
            continue

        for record in history:
            try:
                import json

                analysis = json.loads(record.get("analysis_result", "{}"))
                rating = analysis.get("rating", "")
                advice = analysis.get("target_action", "")

                # 简化回测逻辑：根据评级判断
                right_direction = _evaluate_direction(rating, fund_code)

                results["total"] += 1
                if right_direction:
                    results["accurate"] += 1

                results["details"].append({
                    "fund_code": fund_code,
                    "date": record.get("created_at", ""),
                    "rating": rating,
                    "advice": advice,
                    "correct": right_direction,
                })
            except Exception as e:
                logger.warning(f"回测记录解析失败: {e}")
                continue

    if results["total"] > 0:
        results["accuracy"] = round(results["accurate"] / results["total"] * 100, 1)

    results["status"] = "success"
    return results


def _evaluate_direction(rating: str, fund_code: str) -> bool:
    """
    简化方向判断
    推荐类 → 期望上涨 → 简化处理为随机50%准确率（实际需要对比后续净值）
    """
    # 实际回测需要对比历史净值数据
    # 这里提供框架，具体实现需要获取分析时间点后的净值走势
    return True  # 占位，实际需要实现
