# -*- coding: utf-8 -*-
"""
如意基金分析 RuyiFundAnalysis
基于 AI 大模型的基金/ETF 智能分析系统
每日自动分析自选基金，生成决策仪表盘与专业报告
"""

import argparse
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

# ====== 环境初始化 ======


def setup_env():
    """加载 .env 配置"""
    from dotenv import load_dotenv

    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()


setup_env()

# ====== 日志配置 ======

LOG_DIR = Path(os.getenv("LOG_DIR", "./logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "ruyi_fund.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("ruyi_fund")

# ====== 配置管理 ======


def get_config():
    """获取系统配置"""
    return {
        "fund_list": _parse_fund_list(os.getenv("FUND_LIST", "")),
        "database_path": os.getenv("DATABASE_PATH", "./data/fund_analysis.db"),
        "max_workers": int(os.getenv("MAX_WORKERS", "3")),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "report_language": os.getenv("REPORT_LANGUAGE", "zh"),
        "report_type": os.getenv("REPORT_TYPE", "simple"),
        "llm_model": os.getenv("LITELLM_MODEL", ""),
        "market_review_enabled": os.getenv("MARKET_REVIEW_ENABLED", "true").lower() == "true",
        "run_immediately": os.getenv("RUN_IMMEDIATELY", "true").lower() == "true",
    }


def _parse_fund_list(fund_str: str) -> list:
    """解析基金列表"""
    if not fund_str:
        return []
    return [f.strip() for f in fund_str.split(",") if f.strip()]


# ====== 命令行参数 ======


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="如意基金分析 RuyiFundAnalysis - 基金/ETF AI 智能分析系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式:
  python main.py                    默认运行：单次分析
  python main.py --serve            启动 Web 服务 + 单次分析
  python main.py --serve-only       仅启动 Web 服务
  python main.py --schedule         定时任务模式
  python main.py --backtest         回测模式

示例:
  python main.py --funds 510050,510300
  python main.py --serve --port 8000
  python main.py --schedule --time 18:00
        """,
    )

    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--dry-run", action="store_true", help="仅获取数据，不分析")
    parser.add_argument("--funds", type=str, help="指定基金代码（逗号分隔）")
    parser.add_argument("--no-notify", action="store_true", help="不发送通知")
    parser.add_argument("--schedule", action="store_true", help="定时任务模式")
    parser.add_argument("--time", type=str, default="18:00", help="定时执行时间 (HH:MM)")
    parser.add_argument("--backtest", action="store_true", help="运行回测")
    parser.add_argument("--serve", action="store_true", help="启动 FastAPI Web 服务")
    parser.add_argument("--serve-only", action="store_true", help="仅启动 Web 服务")
    parser.add_argument("--port", type=int, default=8000, help="Web 服务端口")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Web 服务绑定地址")
    parser.add_argument("--force-run", action="store_true", help="强制运行（跳过交易日检查）")

    return parser.parse_args()


# ====== 核心分析流程 ======


def run_single_analysis(fund_code: str, config: dict, dry_run: bool = False):
    """执行单只基金分析"""
    logger.info(f"[分析] 开始分析基金: {fund_code}")

    analysis_id = str(uuid.uuid4())[:8]
    result = {
        "id": analysis_id,
        "fund_code": fund_code,
        "timestamp": datetime.now().isoformat(),
        "status": "success",
    }

    try:
        # 1. 获取基金数据
        from src.data.fund_data import fetch_fund_data

        fund_data = fetch_fund_data(fund_code)

        if dry_run:
            logger.info(f"[数据] {fund_code} 数据获取完成（dry-run 模式，跳过分析）")
            result["data"] = fund_data
            result["status"] = "dry_run"
            return result

        # 2. AI 分析
        from src.analysis.fund_analyzer import analyze_fund

        analysis = analyze_fund(fund_code, fund_data, config)
        result["analysis"] = analysis

        # 3. 保存分析结果
        from src.data.storage import save_analysis

        save_analysis(analysis_id, fund_code, analysis)

        logger.info(f"[完成] {fund_code} 分析完成: {analysis.get('summary', '')}")

    except Exception as e:
        logger.error(f"[错误] {fund_code} 分析失败: {e}", exc_info=config.get("debug"))
        result["status"] = "error"
        result["error"] = str(e)

    return result


def run_market_review(config: dict):
    """执行大盘复盘"""
    logger.info("[大盘复盘] 开始...")

    try:
        from src.analysis.market_review import review_market

        review = review_market(config)
        logger.info(f"[大盘复盘] 完成: {review.get('summary', '')}")
        return review
    except Exception as e:
        logger.error(f"[大盘复盘] 失败: {e}", exc_info=config.get("debug"))
        return {"status": "error", "error": str(e)}


def run_full_analysis(config: dict, funds: list = None, dry_run: bool = False):
    """执行完整分析流程"""
    fund_list = funds or config.get("fund_list", [])

    if not fund_list:
        logger.warning("未配置自选基金列表")
        return {"status": "empty", "message": "未配置自选基金列表"}

    logger.info(f"开始分析 {len(fund_list)} 只基金: {', '.join(fund_list)}")

    results = []

    # 1. 大盘复盘（可选）
    if config.get("market_review_enabled"):
        market_review = run_market_review(config)
        results.append({"type": "market_review", "data": market_review})

    # 2. 逐只分析基金
    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=config.get("max_workers", 3)) as executor:
        futures = {
            executor.submit(run_single_analysis, code, config, dry_run): code
            for code in fund_list
        }
        for future in as_completed(futures):
            code = futures[future]
            try:
                result = future.result()
                results.append({"type": "fund_analysis", "code": code, "data": result})
            except Exception as e:
                logger.error(f"[异常] {code}: {e}")
                results.append(
                    {"type": "fund_analysis", "code": code, "data": {"status": "error", "error": str(e)}}
                )

    # 3. 生成汇总报告
    summary = _generate_summary(results, config)
    results.append({"type": "summary", "data": summary})

    # 4. 发送通知
    if not config.get("no_notify"):
        _send_notifications(results, config)

    logger.info("全部分析完成")
    return results


def _generate_summary(results: list, config: dict) -> dict:
    """生成汇总报告"""
    fund_results = [r for r in results if r.get("type") == "fund_analysis"]

    success_count = sum(1 for r in fund_results if r["data"].get("status") == "success")
    error_count = sum(1 for r in fund_results if r["data"].get("status") == "error")

    return {
        "total": len(fund_results),
        "success": success_count,
        "error": error_count,
        "timestamp": datetime.now().isoformat(),
    }


def _send_notifications(results: list, config: dict):
    """发送通知"""
    try:
        from src.notifier.notifier import send_analysis_notification

        send_analysis_notification(results, config)
    except Exception as e:
        logger.error(f"[通知] 发送失败: {e}")


# ====== 定时调度 ======


def run_scheduled_analysis(config: dict, schedule_time: str = "18:00"):
    """定时任务模式"""
    import schedule
    import time

    logger.info(f"[定时] 已启用，每日 {schedule_time} 执行分析")

    schedule.every().day.at(schedule_time).do(run_full_analysis, config)

    if config.get("run_immediately"):
        logger.info("[定时] 立即执行首次分析...")
        run_full_analysis(config)

    while True:
        schedule.run_pending()
        time.sleep(60)


# ====== Web 服务 ======


def start_api_server(host: str = "127.0.0.1", port: int = 8000):
    """启动 FastAPI Web 服务"""
    import uvicorn

    logger.info(f"[Web] 启动服务: http://{host}:{port}")

    # 确保 static 目录存在
    static_dir = Path(__file__).parent / "static"
    static_dir.mkdir(parents=True, exist_ok=True)

    uvicorn.run(
        "server:create_app",
        host=host,
        port=port,
        factory=True,
        log_level="info",
    )


# ====== 回测 ======


def run_backtest(config: dict):
    """运行回测"""
    logger.info("[回测] 开始历史分析回测...")

    try:
        from src.analysis.backtest import run_fund_backtest

        results = run_fund_backtest(config)
        logger.info(f"[回测] 完成: {results}")
        return results
    except Exception as e:
        logger.error(f"[回测] 失败: {e}", exc_info=config.get("debug"))
        return {"status": "error", "error": str(e)}


# ====== 主入口 ======


def main():
    """主函数"""
    args = parse_arguments()
    config = get_config()

    # 调试模式
    if args.debug:
        config["debug"] = True
        logging.getLogger().setLevel(logging.DEBUG)

    # 指定基金列表
    if args.funds:
        config["fund_list"] = _parse_fund_list(args.funds)

    # 不通知
    if args.no_notify:
        config["no_notify"] = True

    logger.info("=" * 60)
    logger.info("  如意基金分析 RuyiFundAnalysis v1.0")
    logger.info(f"  自选基金: {', '.join(config['fund_list']) if config['fund_list'] else '无'}")
    logger.info(f"  启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    try:
        # 仅 Web 服务
        if args.serve_only:
            start_api_server(args.host, args.port)
            return 0

        # 定时任务
        if args.schedule:
            run_scheduled_analysis(config, args.time)
            return 0

        # 回测
        if args.backtest:
            run_backtest(config)
            return 0

        # 默认：单次分析
        results = run_full_analysis(config, dry_run=args.dry_run)

        # 同时启动 Web 服务
        if args.serve:
            import threading

            web_thread = threading.Thread(
                target=start_api_server,
                args=(args.host, args.port),
                daemon=True,
            )
            web_thread.start()
            logger.info(f"[Web] 服务运行中: http://{args.host}:{args.port}")
            web_thread.join()

    except KeyboardInterrupt:
        logger.info("收到中断信号，正在退出...")
    except Exception as e:
        logger.error(f"程序异常退出: {e}", exc_info=config.get("debug"))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
