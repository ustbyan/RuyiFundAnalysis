import { useState, useEffect } from "react";
import { RiBarChartBoxLine, RiCoinsLine } from "@remixicon/react";
import { getLLMUsage } from "@/utils/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const COLORS = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"];

export default function Usage() {
  const [period, setPeriod] = useState("today");
  const [usageData, setUsageData] = useState<any>(null);

  useEffect(() => {
    loadUsage();
  }, [period]);

  const loadUsage = async () => {
    try {
      const res = await getLLMUsage(period);
      setUsageData(res.data.data);
    } catch (err) {
      console.error(err);
    }
  };

  // 模拟数据
  const mockPieData = [
    { name: "问基 Agent", value: 35000 },
    { name: "基金分析", value: 52000 },
    { name: "大盘复盘", value: 15000 },
    { name: "报告生成", value: 8000 },
    { name: "其他", value: 5000 },
  ];

  const mockBarData = Array.from({ length: 7 }, (_, i) => ({
    day: `D-${6 - i}`,
    问基Agent: 3000 + Math.random() * 5000,
    基金分析: 5000 + Math.random() * 8000,
    大盘复盘: 1000 + Math.random() * 3000,
  }));

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-cyan-500/10">
          <RiBarChartBoxLine className="w-6 h-6 text-cyan-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold">用量监控</h1>
          <p className="text-sm text-gray-400 mt-0.5">实时统计 LLM Token 消耗</p>
        </div>
      </div>

      {/* 时间筛选 */}
      <div className="flex gap-2">
        {["today", "week", "month", "all"].map((p) => (
          <button
            key={p}
            onClick={() => setPeriod(p)}
            className={`px-4 py-2 rounded-lg text-sm transition-all ${
              period === p
                ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30"
                : "bg-white/5 text-gray-400 border border-white/5 hover:border-white/10"
            }`}
          >
            {p === "today" ? "今日" : p === "week" ? "本周" : p === "month" ? "本月" : "全部"}
          </button>
        ))}
      </div>

      {/* 总览 */}
      <div className="grid grid-cols-3 gap-4">
        <div className="glass-card p-4">
          <div className="flex items-center gap-2 text-xs text-gray-500 mb-2">
            <RiCoinsLine className="w-3.5 h-3.5" />
            总 Token 消耗
          </div>
          <div className="text-2xl font-bold text-gray-100">
            {usageData?.total_tokens?.toLocaleString() || "115,000"}
          </div>
        </div>
        <div className="glass-card p-4">
          <div className="text-xs text-gray-500 mb-2">API 调用次数</div>
          <div className="text-2xl font-bold text-gray-100">328</div>
        </div>
        <div className="glass-card p-4">
          <div className="text-xs text-gray-500 mb-2">活跃模型数</div>
          <div className="text-2xl font-bold text-gray-100">3</div>
        </div>
      </div>

      {/* 图表区 */}
      <div className="grid grid-cols-2 gap-4">
        {/* 按类型分布 */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-medium text-gray-400 mb-4">按类型分布</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={mockPieData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                paddingAngle={3}
                dataKey="value"
              >
                {mockPieData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "rgba(30,41,59,0.95)",
                  border: "1px solid rgba(148,163,184,0.2)",
                  borderRadius: "8px",
                  color: "#e2e8f0",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex flex-wrap gap-3 justify-center mt-2">
            {mockPieData.map((item, i) => (
              <div key={i} className="flex items-center gap-1.5 text-xs">
                <span
                  className="w-2.5 h-2.5 rounded-full"
                  style={{ background: COLORS[i % COLORS.length] }}
                />
                <span className="text-gray-400">{item.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 每日趋势 */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-medium text-gray-400 mb-4">近7日趋势</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={mockBarData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
              <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip
                contentStyle={{
                  background: "rgba(30,41,59,0.95)",
                  border: "1px solid rgba(148,163,184,0.2)",
                  borderRadius: "8px",
                  color: "#e2e8f0",
                }}
              />
              <Bar dataKey="问基Agent" fill="#8b5cf6" radius={[4, 4, 0, 0]} stackId="a" />
              <Bar dataKey="基金分析" fill="#3b82f6" radius={[0, 0, 0, 0]} stackId="a" />
              <Bar dataKey="大盘复盘" fill="#10b981" radius={[0, 0, 4, 4]} stackId="a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
