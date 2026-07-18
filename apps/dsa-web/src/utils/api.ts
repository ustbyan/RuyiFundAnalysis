import axios from "axios";

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
});

// 分析
export const analyzeFund = (fundCode: string) =>
  api.post(`/analyze/${fundCode}`);

export const batchAnalyze = (fundCodes: string[]) =>
  api.post("/analyze/batch", fundCodes);

export const getAnalysisHistory = (fundCode?: string, limit = 20) =>
  api.get("/analysis/history", { params: { fund_code: fundCode, limit } });

export const getMarketReview = () => api.get("/market-review");

// 基金
export const searchFunds = (keyword: string) =>
  api.get("/funds/search", { params: { keyword } });

export const getFundInfo = (fundCode: string) =>
  api.get(`/funds/${fundCode}/info`);

export const getMarketIndices = () => api.get("/market/indices");

// 自选
export const getWatchlist = () => api.get("/watchlist");

export const addToWatchlist = (item: {
  fund_code: string;
  fund_name?: string;
  fund_type?: string;
}) => api.post("/watchlist", item);

export const removeFromWatchlist = (fundCode: string) =>
  api.delete(`/watchlist/${fundCode}`);

// 持仓
export const getPortfolio = (account = "默认账户") =>
  api.get("/portfolio", { params: { account } });

export const updatePortfolio = (item: {
  fund_code: string;
  fund_name?: string;
  shares: number;
  cost_price: number;
}) => api.post("/portfolio", item);

// 设置
export const getSettings = () => api.get("/settings");

export const updateSettings = (settings: Record<string, unknown>) =>
  api.post("/settings", settings);

export const checkConnection = () =>
  api.post("/settings/check-connection");

// 用量
export const getLLMUsage = (period = "today") =>
  api.get("/usage/llm", { params: { period } });

// 告警
export const getAlerts = () => api.get("/alerts");

export const createAlert = (alert: {
  fund_code: string;
  alert_type: string;
  threshold: number;
  direction: string;
}) => api.post("/alerts", alert);

export default api;
