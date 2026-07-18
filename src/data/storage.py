# -*- coding: utf-8 -*-
"""
如意基金分析 - 数据存储模块
使用 SQLite 存储分析历史、自选列表、持仓记录等
"""

import json
import logging
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("DATABASE_PATH", "./data/fund_analysis.db")


def _get_connection() -> sqlite3.Connection:
    """获取数据库连接"""
    db_dir = Path(DB_PATH).parent
    db_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_database():
    """初始化数据库表"""
    conn = _get_connection()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id TEXT PRIMARY KEY,
                fund_code TEXT NOT NULL,
                fund_name TEXT,
                analysis_result TEXT,
                summary TEXT,
                rating TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_code TEXT NOT NULL UNIQUE,
                fund_name TEXT,
                fund_type TEXT,
                group_name TEXT DEFAULT '默认',
                sort_order INTEGER DEFAULT 0,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_name TEXT DEFAULT '默认账户',
                fund_code TEXT NOT NULL,
                fund_name TEXT,
                shares REAL DEFAULT 0,
                cost_price REAL DEFAULT 0,
                current_price REAL DEFAULT 0,
                market_value REAL DEFAULT 0,
                profit_loss REAL DEFAULT 0,
                profit_loss_pct REAL DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fund_code TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                threshold REAL,
                direction TEXT,
                enabled INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS llm_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                tokens INTEGER DEFAULT 0,
                usage_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_analysis_fund ON analysis_history(fund_code);
            CREATE INDEX IF NOT EXISTS idx_analysis_date ON analysis_history(created_at);
            CREATE INDEX IF NOT EXISTS idx_watchlist_order ON watchlist(sort_order);
            CREATE INDEX IF NOT EXISTS idx_portfolio_account ON portfolio(account_name);
        """)
        conn.commit()
        logger.info("数据库初始化完成")
    finally:
        conn.close()


def save_analysis(analysis_id: str, fund_code: str, analysis: dict):
    """保存分析结果"""
    conn = _get_connection()
    try:
        conn.execute(
            """INSERT OR REPLACE INTO analysis_history 
               (id, fund_code, fund_name, analysis_result, summary, rating)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                analysis_id,
                fund_code,
                analysis.get("fund_name", ""),
                json.dumps(analysis, ensure_ascii=False),
                analysis.get("summary", ""),
                analysis.get("rating", ""),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_analysis_history(fund_code: str = None, limit: int = 50) -> list:
    """获取分析历史"""
    conn = _get_connection()
    try:
        if fund_code:
            rows = conn.execute(
                "SELECT * FROM analysis_history WHERE fund_code = ? ORDER BY created_at DESC LIMIT ?",
                (fund_code, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM analysis_history ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()

        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_watchlist() -> list:
    """获取自选列表"""
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM watchlist ORDER BY sort_order, id"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def add_to_watchlist(
    fund_code: str,
    fund_name: str = "",
    fund_type: str = "",
    group_name: str = "默认",
):
    """添加自选基金"""
    conn = _get_connection()
    try:
        conn.execute(
            """INSERT OR REPLACE INTO watchlist (fund_code, fund_name, fund_type, group_name)
               VALUES (?, ?, ?, ?)""",
            (fund_code, fund_name, fund_type, group_name),
        )
        conn.commit()
    finally:
        conn.close()


def remove_from_watchlist(fund_code: str):
    """移除自选基金"""
    conn = _get_connection()
    try:
        conn.execute("DELETE FROM watchlist WHERE fund_code = ?", (fund_code,))
        conn.commit()
    finally:
        conn.close()


def get_portfolio(account_name: str = "默认账户") -> list:
    """获取持仓列表"""
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM portfolio WHERE account_name = ? ORDER BY market_value DESC",
            (account_name,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def update_portfolio(
    fund_code: str,
    fund_name: str,
    shares: float,
    cost_price: float,
    account_name: str = "默认账户",
):
    """更新持仓"""
    conn = _get_connection()
    try:
        current_price = cost_price  # 简化处理
        market_value = shares * current_price
        profit_loss = 0  # 需要实时价格计算

        conn.execute(
            """INSERT OR REPLACE INTO portfolio 
               (account_name, fund_code, fund_name, shares, cost_price, current_price, market_value)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (account_name, fund_code, fund_name, shares, cost_price, current_price, market_value),
        )
        conn.commit()
    finally:
        conn.close()


def log_llm_usage(model: str, tokens: int, usage_type: str = "analysis"):
    """记录 LLM Token 用量"""
    conn = _get_connection()
    try:
        conn.execute(
            "INSERT INTO llm_usage (model, tokens, usage_type) VALUES (?, ?, ?)",
            (model, tokens, usage_type),
        )
        conn.commit()
    finally:
        conn.close()


def get_llm_usage_summary(period: str = "today") -> dict:
    """获取 LLM 用量汇总"""
    conn = _get_connection()
    try:
        if period == "today":
            date_filter = "date(created_at) = date('now')"
        elif period == "month":
            date_filter = "strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')"
        else:
            date_filter = "1=1"

        rows = conn.execute(
            f"""SELECT model, usage_type, SUM(tokens) as total_tokens
                FROM llm_usage WHERE {date_filter}
                GROUP BY model, usage_type""",
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


# 启动时自动初始化
init_database()
