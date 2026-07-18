import { useState } from "react";
import { RiLineChartLine, RiPlayFill, RiCheckLine, RiCloseLine } from "@remixicon/react";
import { motion } from "motion/react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function Backtest() {
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleRun = async () => {
    setRunning(true);
    // 模拟回测
    await new Promise((resolve) => setTimeout(resolve, 2000));

    const mockData = {
      total_trades: 120,
      win_rate: 58.3,
      total_return: 23.5,
      max_drawdown: -12.8,
      sharpe_ratio: 1.42,
      win_rate_trend: Array.from({ length: 12 }, (_, i) => ({
        month: `${i + 1}月`,
        winRate: 40 + Math.random() * 40,
        return: -10 + Math.random() * 30,
      })),
    };

    setResults(mockData);
    setRunning(false);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-rose-500/10">
          <RiLineChartLine className="w-6 h-6 text-rose-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold">回测分析</h1>
          <p className="text-sm text-gray-400 mt-0.5">验证历史分析准确率</p>
        </div>
      </div>

      {/* 回测控制 */}
      <div className="glass-card p-6 text-center">
        <p className="text-gray-400 mb-4">
          回测将对比历史分析结果与后续实际表现，评估分析准确率
        </p>
        <button
          onClick={handleRun}
          disabled={running}
          className="inline-flex items-center gap-2 px-6 py-3 bg-rose-500 hover:bg-rose-600 disabled:bg-gray-700 text-white rounded-xl transition-all"
        >
          {running ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              回测中...
            </>
          ) : (
            <>
              <RiPlayFill className="w-5 h-5" />
              开始回测
            </>
          )}
        </button>
      </div>

      {/* 回测结果 */}
      {results && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          {/* 核心指标 */}
          <div className="grid grid-cols-5 gap-4">
            {[
              { label: "总交易次数", value: results.total_trades },
              { label: "胜率", value: `${results.win_rate}%` },
              { label: "总收益", value: `${results.total_return > 0 ? "+" : ""}${results.total_return}%` },
              { label: "最大回撤", value: `${results.max_drawdown}%` },
              { label: "夏普比率", value: results.sharpe_ratio },
            ].map((item, i) => (
              <div key={i} className="glass-card p-4 text-center">
                <div className="text-xs text-gray-500">{item.label}</div>
                <div
                  className={`text-xl font-bold mt-1 ${
                    typeof item.value === "string" && item.value.includes("-")
                      ? "text-green-400"
                      : "text-gray-100"
                  }`}
                >
                  {item.value}
                </div>
              </div>
            ))}
          </div>

          {/* 趋势图 */}
          <div className="glass-card p-5">
            <h3 className="text-sm font-medium text-gray-400 mb-4">月度表现趋势</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={results.win_rate_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    background: "rgba(30,41,59,0.95)",
                    border: "1px solid rgba(148,163,184,0.2)",
                    borderRadius: "8px",
                    color: "#e2e8f0",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="winRate"
                  stroke="#f43f5e"
                  strokeWidth={2}
                  name="胜率(%)"
                  dot={{ r: 3 }}
                />
                <Line
                  type="monotone"
                  dataKey="return"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  name="收益(%)"
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      )}
    </div>
  );
}
