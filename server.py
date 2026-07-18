# -*- coding: utf-8 -*-
"""
如意基金分析 - FastAPI 服务
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="如意基金分析 RuyiFundAnalysis",
        description="基金/ETF AI 智能分析系统 API",
        version="1.0.0",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册 API 路由
    from src.api.v1.endpoints import (
        analysis,
        funds,
        watchlist,
        portfolio,
        settings,
        alerts,
        usage,
    )

    app.include_router(analysis.router, prefix="/api/v1", tags=["分析"])
    app.include_router(funds.router, prefix="/api/v1", tags=["基金"])
    app.include_router(watchlist.router, prefix="/api/v1", tags=["自选"])
    app.include_router(portfolio.router, prefix="/api/v1", tags=["持仓"])
    app.include_router(settings.router, prefix="/api/v1", tags=["设置"])
    app.include_router(alerts.router, prefix="/api/v1", tags=["告警"])
    app.include_router(usage.router, prefix="/api/v1", tags=["用量"])

    # 健康检查
    @app.get("/api/health")
    async def health_check():
        return {"status": "ok", "version": "1.0.0"}

    # 静态文件（前端构建产物）
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")

        @app.get("/{full_path:path}")
        async def serve_frontend(full_path: str):
            """服务前端 SPA"""
            file_path = static_dir / full_path
            if file_path.exists() and file_path.is_file():
                return FileResponse(str(file_path))
            return FileResponse(str(static_dir / "index.html"))

    return app
