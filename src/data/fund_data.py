# -*- coding: utf-8 -*-
"""
如意基金分析 - 基金数据采集模块
数据源优先级: efinance > akshare > tushare
"""

import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


def fetch_fund_data(fund_code: str, prefer_source: str = "auto") -> dict:
    """
    获取基金综合数据
    
    Args:
        fund_code: 基金代码（如 510050, 000011）
        prefer_source: 优先数据源（auto/efinance/akshare/tushare）
    
    Returns:
        包含基金基本信息、净值、业绩、持仓等数据的字典
    """
    data = {
        "fund_code": fund_code,
        "source": "unknown",
        "basic_info": {},
        "nav_data": None,
        "performance": {},
        "holdings": [],
        "manager_info": {},
        "market_data": {},
    }

    # 尝试按优先级获取数据
    sources = _get_source_order(prefer_source)

    for source in sources:
        try:
            logger.debug(f"[数据] 尝试 {source} 获取 {fund_code}")

            if source == "efinance":
                _fetch_from_efinance(fund_code, data)
            elif source == "akshare":
                _fetch_from_akshare(fund_code, data)
            elif source == "tushare":
                _fetch_from_tushare(fund_code, data)

            if data.get("basic_info"):
                data["source"] = source
                logger.info(f"[数据] {fund_code} 获取成功 (来源: {source})")
                break
        except Exception as e:
            logger.warning(f"[数据] {source} 获取 {fund_code} 失败: {e}")
            continue

    return data


def _get_source_order(prefer: str) -> list:
    """获取数据源优先级顺序"""
    if prefer == "efinance":
        return ["efinance", "akshare", "tushare"]
    elif prefer == "akshare":
        return ["akshare", "efinance", "tushare"]
    elif prefer == "tushare":
        return ["tushare", "efinance", "akshare"]
    else:
        return ["efinance", "akshare", "tushare"]


def _fetch_from_efinance(fund_code: str, data: dict):
    """从 efinance 获取基金数据"""
    try:
        import efinance as ef

        # 获取基金基本信息
        info = ef.fund.get_base_info(fund_code)
        if info is not None:
            data["basic_info"] = {
                "name": info.get("基金简称", ""),
                "type": info.get("基金类型", ""),
                "manager": info.get("基金经理", ""),
                "company": info.get("基金公司", ""),
                "scale": info.get("基金规模", ""),
                "establish_date": info.get("成立日期", ""),
            }

        # 获取净值数据
        try:
            nav = ef.fund.get_quote_history(fund_code)
            if nav is not None and not nav.empty:
                data["nav_data"] = nav.tail(252)  # 近一年数据
        except Exception:
            pass

    except ImportError:
        logger.warning("efinance 未安装")
    except Exception as e:
        logger.warning(f"efinance 获取 {fund_code} 失败: {e}")


def _fetch_from_akshare(fund_code: str, data: dict):
    """从 akshare 获取基金数据"""
    try:
        import akshare as ak

        # 场内 ETF 数据
        if fund_code.startswith(("51", "15", "16")):
            try:
                info = ak.fund_etf_fund_info_em(fund=fund_code)
                if info is not None and not info.empty:
                    row = info.iloc[0]
                    data["basic_info"] = {
                        "name": row.get("基金简称", ""),
                        "type": "ETF",
                        "manager": row.get("基金经理", ""),
                        "company": row.get("基金管理人", ""),
                        "scale": row.get("基金规模", ""),
                    }
            except Exception:
                pass

        # 场外基金数据
        else:
            try:
                info = ak.fund_open_fund_info_em(fund=fund_code, indicator="单位净值走势")
                if info is not None and not info.empty:
                    data["nav_data"] = info
            except Exception:
                pass

        # 基金名称
        try:
            name_df = ak.fund_name_em()
            if name_df is not None:
                match = name_df[name_df["基金代码"] == fund_code]
                if not match.empty:
                    data["basic_info"]["name"] = data["basic_info"].get("name") or match.iloc[0]["基金简称"]
        except Exception:
            pass

    except ImportError:
        logger.warning("akshare 未安装")
    except Exception as e:
        logger.warning(f"akshare 获取 {fund_code} 失败: {e}")


def _fetch_from_tushare(fund_code: str, data: dict):
    """从 Tushare 获取基金数据"""
    import os

    token = os.getenv("TUSHARE_TOKEN")
    if not token:
        raise ValueError("未配置 TUSHARE_TOKEN")

    try:
        import tushare as ts

        pro = ts.pro_api(token)
        # Tushare 基金数据接口
        df = pro.fund_basic(ts_code=fund_code)
        if df is not None and not df.empty:
            row = df.iloc[0]
            data["basic_info"] = {
                "name": row.get("name", ""),
                "type": row.get("fund_type", ""),
                "manager": row.get("manager", ""),
                "company": row.get("management", ""),
                "establish_date": row.get("found_date", ""),
            }
    except ImportError:
        logger.warning("tushare 未安装")
    except Exception as e:
        logger.warning(f"tushare 获取 {fund_code} 失败: {e}")


def fetch_fund_news(fund_code: str, days: int = 7) -> list:
    """获取基金相关新闻"""
    news_list = []
    try:
        import akshare as ak
        from datetime import datetime, timedelta

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        try:
            news_df = ak.fund_news_em(date=end_date)
            if news_df is not None and not news_df.empty:
                for _, row in news_df.head(10).iterrows():
                    news_list.append({
                        "title": row.get("标题", ""),
                        "time": row.get("时间", ""),
                        "source": row.get("来源", ""),
                    })
        except Exception:
            pass
    except Exception as e:
        logger.warning(f"获取新闻失败: {e}")

    return news_list


def search_funds(keyword: str) -> list:
    """搜索基金"""
    results = []
    try:
        import akshare as ak

        name_df = ak.fund_name_em()
        if name_df is not None:
            matches = name_df[
                name_df["基金简称"].str.contains(keyword, na=False)
                | name_df["基金代码"].str.contains(keyword, na=False)
            ]
            for _, row in matches.head(20).iterrows():
                results.append({
                    "code": row["基金代码"],
                    "name": row["基金简称"],
                    "type": row.get("基金类型", ""),
                })
    except Exception as e:
        logger.warning(f"搜索基金失败: {e}")

    return results


def fetch_market_index() -> dict:
    """获取市场指数数据"""
    indices = {}
    try:
        import akshare as ak

        index_map = {
            "上证指数": "000001",
            "深证成指": "399001",
            "创业板指": "399006",
            "沪深300": "000300",
            "科创50": "000688",
        }

        for name, code in index_map.items():
            try:
                df = ak.stock_zh_index_daily(symbol=f"sh{code}")
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    indices[name] = {
                        "close": float(latest.get("close", 0)),
                        "change_pct": float(latest.get("pct_chg", 0)),
                        "volume": float(latest.get("volume", 0)),
                    }
            except Exception:
                continue
    except Exception as e:
        logger.warning(f"获取市场指数失败: {e}")

    return indices
