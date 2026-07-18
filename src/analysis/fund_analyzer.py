# -*- coding: utf-8 -*-
"""
如意基金分析 - 基金分析引擎
包含技术面、基本面、AI 综合研判
"""

import json
import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def analyze_fund(fund_code: str, fund_data: dict, config: dict) -> dict:
    """
    综合分析基金
    
    Args:
        fund_code: 基金代码
        fund_data: 采集的基金数据
        config: 系统配置
    
    Returns:
        分析结果字典，包含评分、摘要、建议等
    """
    basic_info = fund_data.get("basic_info", {})
    fund_name = basic_info.get("name", fund_code)

    result = {
        "fund_code": fund_code,
        "fund_name": fund_name,
        "timestamp": datetime.now().isoformat(),
        "rating": "",
        "summary": "",
        "scores": {},
        "advice": {},
        "risks": [],
        "highlights": [],
    }

    # 1. 技术面分析（净值趋势）
    tech_score = _technical_analysis(fund_data)
    result["scores"]["technical"] = tech_score
    result["risks"].extend(tech_score.get("risks", []))
    result["highlights"].extend(tech_score.get("highlights", []))

    # 2. 基本面分析
    fundamental_score = _fundamental_analysis(fund_data)
    result["scores"]["fundamental"] = fundamental_score
    result["risks"].extend(fundamental_score.get("risks", []))
    result["highlights"].extend(fundamental_score.get("highlights", []))

    # 3. AI 综合研判
    ai_analysis = _ai_comprehensive_analysis(fund_code, fund_name, fund_data, tech_score, fundamental_score, config)
    result["ai_analysis"] = ai_analysis
    result["summary"] = ai_analysis.get("summary", "分析完成")
    result["rating"] = ai_analysis.get("rating", "")

    # 4. 综合评分
    result["overall_score"] = _calculate_overall_score(tech_score, fundamental_score, ai_analysis)

    return result


def _technical_analysis(fund_data: dict) -> dict:
    """技术面分析（净值趋势、均线、成交量等）"""
    nav_data = fund_data.get("nav_data")
    result = {"score": 50, "risks": [], "highlights": [], "details": {}}

    if nav_data is None or nav_data.empty:
        result["details"]["status"] = "无净值数据"
        return result

    try:
        import pandas as pd
        import numpy as np

        # 确保有净值列
        nav_col = None
        for col in ["单位净值", "累计净值", "nav", "close", "净值"]:
            if col in nav_data.columns:
                nav_col = col
                break
        if nav_col is None:
            nav_col = nav_data.select_dtypes(include=[np.number]).columns[0]

        nav_series = nav_data[nav_col].dropna()

        if len(nav_series) < 5:
            result["details"]["status"] = "数据不足"
            return result

        latest_nav = nav_series.iloc[-1]

        # MA5, MA10, MA20
        ma5 = nav_series.rolling(5).mean().iloc[-1]
        ma10 = nav_series.rolling(10).mean().iloc[-1]
        ma20 = nav_series.rolling(20).mean().iloc[-1]

        result["details"]["latest_nav"] = round(float(latest_nav), 4)
        result["details"]["ma5"] = round(float(ma5), 4) if not pd.isna(ma5) else None
        result["details"]["ma10"] = round(float(ma10), 4) if not pd.isna(ma10) else None
        result["details"]["ma20"] = round(float(ma20), 4) if not pd.isna(ma20) else None

        # 多头排列判断
        if not pd.isna(ma5) and not pd.isna(ma10) and not pd.isna(ma20):
            if ma5 > ma10 > ma20 and latest_nav > ma5:
                result["score"] += 20
                result["highlights"].append("净值多头排列，趋势向好")
                result["details"]["trend"] = "bullish"
            elif ma5 < ma10 < ma20 and latest_nav < ma5:
                result["score"] -= 20
                result["risks"].append("净值空头排列，趋势偏弱")
                result["details"]["trend"] = "bearish"
            else:
                result["details"]["trend"] = "neutral"

        # 近期涨跌幅
        if len(nav_series) >= 20:
            pct_5d = (nav_series.iloc[-1] / nav_series.iloc[-6] - 1) * 100
            pct_20d = (nav_series.iloc[-1] / nav_series.iloc[-21] - 1) * 100
            result["details"]["pct_5d"] = round(float(pct_5d), 2)
            result["details"]["pct_20d"] = round(float(pct_20d), 2)

            if pct_5d > 5:
                result["risks"].append(f"近5日涨幅 {pct_5d:.1f}%，短期追高风险")
            if pct_20d < -10:
                result["highlights"].append(f"近20日跌幅较大 {pct_20d:.1f}%，可能存在超跌机会")

    except Exception as e:
        logger.warning(f"技术面分析异常: {e}")
        result["details"]["error"] = str(e)

    return result


def _fundamental_analysis(fund_data: dict) -> dict:
    """基本面分析（基金规模、费率、经理、持仓等）"""
    basic_info = fund_data.get("basic_info", {})
    result = {"score": 50, "risks": [], "highlights": [], "details": {}}

    # 基金规模评估
    scale_str = basic_info.get("scale", "")
    try:
        # 尝试解析规模数字
        scale_num = _parse_scale(scale_str)
        result["details"]["scale"] = scale_str
        if scale_num and scale_num > 100:
            result["score"] += 10
            result["highlights"].append(f"基金规模 {scale_str}，流动性好")
        elif scale_num and scale_num < 1:
            result["score"] -= 10
            result["risks"].append(f"基金规模仅 {scale_str}，存在清盘风险")
    except Exception:
        pass

    # 基金类型评估
    fund_type = basic_info.get("type", "")
    result["details"]["type"] = fund_type

    if "ETF" in fund_type or "指数" in fund_type:
        result["score"] += 5
        result["details"]["type_score"] = "被动型基金，费率通常较低"
    elif "混合" in fund_type:
        result["details"]["type_score"] = "混合型基金，取决于经理能力"
    elif "债券" in fund_type or "货币" in fund_type:
        result["score"] += 5
        result["details"]["type_score"] = "固收类基金，风险较低"

    # 基金经理
    manager = basic_info.get("manager", "")
    if manager:
        result["details"]["manager"] = manager
        result["details"]["manager_score"] = "基金经理信息已记录"

    # 基金公司
    company = basic_info.get("company", "")
    if company:
        result["details"]["company"] = company

    return result


def _ai_comprehensive_analysis(
    fund_code: str,
    fund_name: str,
    fund_data: dict,
    tech_score: dict,
    fundamental_score: dict,
    config: dict,
) -> dict:
    """
    AI 大模型综合分析
    使用 LiteLLM 调用大模型进行综合研判
    """
    result = {
        "summary": "",
        "rating": "",
        "advice": "",
        "key_points": [],
        "model": "",
    }

    try:
        from litellm import completion

        # 构建提示词
        prompt = _build_analysis_prompt(fund_code, fund_name, fund_data, tech_score, fundamental_score)

        # 获取模型配置
        model = config.get("llm_model") or os.getenv("LITELLM_MODEL", "")

        if not model:
            # 自动检测可用模型
            if os.getenv("DEEPSEEK_API_KEY"):
                model = "deepseek/deepseek-chat"
            elif os.getenv("GEMINI_API_KEY"):
                model = "gemini/gemini-2.0-flash"
            elif os.getenv("OPENAI_API_KEY"):
                model = "openai/gpt-4o-mini"
            else:
                # 无 API Key，使用模拟分析
                return _mock_ai_analysis(fund_code, fund_name, tech_score, fundamental_score)

        result["model"] = model

        response = completion(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的基金分析师。请用中文回答，输出JSON格式。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        content = response.choices[0].message.content or ""

        # 记录用量
        try:
            tokens = response.usage.total_tokens if response.usage else 0
            from src.data.storage import log_llm_usage

            log_llm_usage(model, tokens, "fund_analysis")
        except Exception:
            pass

        # 解析AI响应
        ai_result = _parse_ai_response(content)
        result.update(ai_result)

    except ImportError:
        logger.warning("litellm 未安装，使用模拟分析")
        return _mock_ai_analysis(fund_code, fund_name, tech_score, fundamental_score)
    except Exception as e:
        logger.error(f"AI分析异常: {e}")
        result["summary"] = f"AI分析暂时不可用: {str(e)[:100]}"
        result["rating"] = "N/A"

    return result


def _build_analysis_prompt(
    fund_code: str,
    fund_name: str,
    fund_data: dict,
    tech_score: dict,
    fundamental_score: dict,
) -> str:
    """构建分析提示词"""
    basic_info = fund_data.get("basic_info", {})

    prompt = f"""请分析以下基金，并返回JSON格式的分析结果。

基金代码: {fund_code}
基金名称: {fund_name}
基金类型: {basic_info.get('type', '未知')}
基金规模: {basic_info.get('scale', '未知')}
基金经理: {basic_info.get('manager', '未知')}
基金公司: {basic_info.get('company', '未知')}

技术面评分: {tech_score.get('score', 0)}/100
技术面细节: {json.dumps(tech_score.get('details', {}), ensure_ascii=False)}
技术面亮点: {', '.join(tech_score.get('highlights', []))}
技术面风险: {', '.join(tech_score.get('risks', []))}

基本面评分: {fundamental_score.get('score', 0)}/100
基本面亮点: {', '.join(fundamental_score.get('highlights', []))}
基本面风险: {', '.join(fundamental_score.get('risks', []))}

请返回精确的JSON格式（不要包含markdown代码块标记）:
{{
    "rating": "强烈推荐/推荐/中性/谨慎/回避",
    "summary": "100字以内的综合分析摘要",
    "advice": "具体的操作建议",
    "key_points": ["要点1", "要点2", "要点3"],
    "target_action": "买入/持有/减仓/观望",
    "confidence": 0.0-1.0之间的置信度
}}"""
    return prompt


def _parse_ai_response(content: str) -> dict:
    """解析AI响应"""
    try:
        # 尝试直接解析JSON
        data = json.loads(content)
        return {
            "rating": data.get("rating", ""),
            "summary": data.get("summary", ""),
            "advice": data.get("advice", ""),
            "key_points": data.get("key_points", []),
            "target_action": data.get("target_action", ""),
            "confidence": data.get("confidence", 0.5),
        }
    except json.JSONDecodeError:
        # 尝试提取JSON
        try:
            import re
            match = re.search(r"\{[\s\S]*\}", content)
            if match:
                data = json.loads(match.group())
                return {
                    "rating": data.get("rating", ""),
                    "summary": data.get("summary", ""),
                    "advice": data.get("advice", ""),
                    "key_points": data.get("key_points", []),
                    "target_action": data.get("target_action", ""),
                    "confidence": data.get("confidence", 0.5),
                }
        except Exception:
            pass

    return {
        "rating": "N/A",
        "summary": content[:200] if content else "分析结果解析失败",
        "advice": "",
        "key_points": [],
        "target_action": "",
        "confidence": 0,
    }


def _mock_ai_analysis(fund_code: str, fund_name: str, tech_score: dict, fundamental_score: dict) -> dict:
    """模拟AI分析（用于无API Key时的降级方案）"""
    tech_s = tech_score.get("score", 50)
    fund_s = fundamental_score.get("score", 50)
    overall = (tech_s + fund_s) // 2

    if overall >= 75:
        rating = "推荐"
        action = "买入"
    elif overall >= 60:
        rating = "中性偏多"
        action = "持有"
    elif overall >= 40:
        rating = "中性"
        action = "观望"
    else:
        rating = "谨慎"
        action = "减仓"

    return {
        "rating": rating,
        "summary": f"{fund_name}({fund_code}) 综合评分 {overall}/100。技术面 {tech_s} 分，基本面 {fund_s} 分。AI分析暂不可用，以上为规则引擎评估。",
        "advice": f"建议{action}。建议配置API Key获取更精准的AI分析。",
        "key_points": [
            f"技术面评分: {tech_s}/100",
            f"基本面评分: {fund_s}/100",
            "AI分析暂未启用，使用规则引擎评估",
        ],
        "target_action": action,
        "confidence": 0.6,
        "model": "mock_rule_engine",
    }


def _calculate_overall_score(tech_score: dict, fundamental_score: dict, ai_analysis: dict) -> int:
    """计算综合评分"""
    tech_s = tech_score.get("score", 50)
    fund_s = fundamental_score.get("score", 50)
    confidence = ai_analysis.get("confidence", 0.5)

    # 权重：技术面30%，基本面30%，AI置信度加成40%
    base_score = tech_s * 0.3 + fund_s * 0.3 + 50 * 0.4
    ai_bonus = (confidence - 0.5) * 20  # 置信度越高加成越多

    return min(100, max(0, int(base_score + ai_bonus)))


def _parse_scale(scale_str: str) -> Optional[float]:
    """解析基金规模字符串"""
    try:
        scale_str = scale_str.replace(",", "").replace("，", "")
        if "亿" in scale_str:
            return float(scale_str.replace("亿", "").strip())
        elif "万" in scale_str:
            return float(scale_str.replace("万", "").strip()) / 10000
        else:
            return float(scale_str.strip())
    except (ValueError, AttributeError):
        return None
