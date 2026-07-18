# 🏮 如意基金分析 RuyiFundAnalysis

基于 AI 大模型的基金/ETF 智能分析系统 — 每日自动分析自选基金，生成决策仪表盘与专业报告。

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF.svg)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📊 功能概览

| 模块 | 功能描述 |
|------|---------|
| 🏠 智能分析首页 | 输入基金代码，自动采集净值/业绩/持仓/经理数据，AI 综合研判，输出包含评级、操作建议、关键要点的完整报告 |
| 💬 AI 问基 | 对话式交互，AI 可调用实时数据回答基金相关问题 |
| ⭐ 自选管理 | 自定义基金池，支持搜索添加与分组管理 |
| 💼 持仓管理 | 记录基金持仓，跟踪市值与盈亏 |
| 📈 回测模块 | 验证历史分析准确率，可视化月度表现 |
| 🔔 告警中心 | 价格/涨跌幅等多维预警规则 |
| 📊 用量监控 | 实时统计 LLM Token 消耗，按类型拆分明细 |
| ⚙️ 系统设置 | 可视化配置 LLM 通道、通知渠道、自选基金列表 |

## 🏗️ 技术栈

### 后端
- **Python 3.10+** · **FastAPI** · **LiteLLM** (多模型统一网关)
- **SQLAlchemy** (SQLite 数据存储)
- **efinance / akshare / tushare** (基金数据源)
- **LLM 支持**: DeepSeek / OpenAI / Anthropic / Gemini / SiliconFlow / Ollama

### 前端
- **React 19** · **TypeScript** · **Vite 7** · **Tailwind CSS v4**
- **Zustand** (状态管理) · **Recharts** (图表) · **React Router v7**
- **Motion** (动画) · **Lucide/Remix Icon** (图标)

## 📁 项目结构

```
RuyiFundAnalysis/
├── apps/dsa-web/              # React 前端应用
│   ├── src/
│   │   ├── components/        # UI 组件
│   │   ├── pages/             # 页面（首页、AI问基、自选、持仓等）
│   │   ├── stores/            # Zustand 状态管理
│   │   └── utils/             # API 工具
│   ├── package.json
│   └── vite.config.ts
├── src/                       # Python 后端
│   ├── agent/                 # AI Agent 引擎
│   ├── analysis/              # 分析引擎（技术面/基本面/AI研判）
│   ├── data/                  # 数据层（行情采集/存储）
│   ├── api/v1/endpoints/      # REST API 路由
│   └── notifier/              # 通知推送
├── main.py                    # 启动入口
├── server.py                  # FastAPI 服务
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量模板
└── README.md
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/1223wyuwhs/RuyiFundAnalysis.git
cd RuyiFundAnalysis
```

### 2. Python 后端

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，至少填入一种 LLM API Key + 自选基金列表
```

### 3. 配置 API 密钥

至少配置一种 LLM：

```bash
# DeepSeek（推荐，性价比高）
DEEPSEEK_API_KEY=sk-your-key

# Gemini（免费额度）
GEMINI_API_KEY=your-key

# OpenAI
OPENAI_API_KEY=sk-your-key
```

### 4. 前端构建

```bash
cd apps/dsa-web
npm install
npm run build
cd ../..
```

### 5. 启动服务

```bash
# 默认模式：单次分析
python main.py

# 分析 + Web 服务
python main.py --serve

# 仅 Web 服务
python main.py --serve-only

# 定时任务模式
python main.py --schedule --time 18:00
```

浏览器打开 `http://127.0.0.1:8000`

## 💡 使用指南

### 分析基金

1. 在首页输入基金代码（如 510050）
2. 点击「开始分析」
3. 查看 AI 综合研判结果，包含评级、评分、操作建议

### AI 问基

在 AI 问基页面，你可以：
- 直接输入代码让 AI 分析
- 询问基金相关问题
- 获取投资建议

### 自选管理

- 搜索基金代码或名称
- 添加到自选列表
- 一键快捷分析

### 持仓管理

- 手动添加持仓记录（基金代码、份额、成本价）
- 自动计算市值与盈亏
- 持仓汇总一览

## 🔧 LLM 通道配置

| 通道 | 支持模型 | 推荐场景 |
|------|---------|---------|
| DeepSeek | deepseek-chat, deepseek-reasoner | 中文理解优秀，性价比高 |
| Gemini | gemini-2.0-flash, gemini-2.5-pro | 免费额度，多模态能力 |
| OpenAI | gpt-4o, gpt-4o-mini | Function Calling 最稳定 |
| SiliconFlow | DeepSeek-V3, Qwen2.5, GLM-4 | 国内用户，聚合平台 |
| Ollama | qwen3, llama3 等 | 本地部署，数据不外传 |

## 📊 数据源

| 数据源 | 说明 | 费用 |
|--------|------|------|
| efinance | 东方财富接口 | 免费 |
| akshare | 东方财富爬虫 | 免费 |
| tushare | Tushare Pro | 需积分/Token |

优先级: `efinance > akshare > tushare`

## 📢 通知渠道

支持多渠道推送分析结果：

- 企业微信机器人
- 飞书机器人
- 钉钉机器人
- Telegram Bot
- 邮件推送

## 🔐 安全提示

- `.env` 文件包含 API 密钥，切勿提交到版本控制
- 建议使用环境变量或密钥管理服务存储敏感信息
- Web 服务部署到公网时建议启用 `ADMIN_AUTH_ENABLED`

## 📝 许可证

[MIT License](LICENSE) © 2026 张大鹏

---

**如意基金分析 RuyiFundAnalysis** — 让 AI 帮你读懂基金 🏮
