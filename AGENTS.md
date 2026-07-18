# RuyiFundAnalysis - Agent 开发指南

## 项目概述

如意基金分析是一个基于 AI 大模型的基金/ETF 智能分析系统。

## 开发环境

### 后端

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 前端

```bash
cd apps/dsa-web
npm install
npm run dev
```

## 架构说明

### 数据流

1. 用户输入基金代码 → API 路由 → 数据采集层
2. 数据采集层按优先级尝试 efinance/akshare/tushare
3. 分析引擎进行技术面 + 基本面量化评分
4. AI 模型进行综合研判，输出评级与建议
5. 结果存入 SQLite，通过通知渠道推送

### 关键模块

- `src/data/fund_data.py` - 多源数据采集
- `src/analysis/fund_analyzer.py` - 分析引擎
- `src/api/v1/endpoints/` - REST API
- `src/notifier/` - 通知推送
