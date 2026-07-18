import { useState } from "react";
import { RiNotification3Line, RiAddLine, RiDeleteBin6Line, RiToggleLine, RiToggleFill } from "@remixicon/react";

interface Alert {
  id: number;
  fund_code: string;
  alert_type: string;
  threshold: number;
  direction: string;
  enabled: boolean;
}

export default function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    fund_code: "",
    alert_type: "price_cross",
    threshold: 0,
    direction: "above",
  });

  const alertTypes: Record<string, string> = {
    price_cross: "价格突破",
    change_percent: "涨跌幅",
    volume_spike: "成交量放大",
    nav_change: "净值变动",
  };

  const handleAdd = () => {
    if (!form.fund_code || form.threshold <= 0) return;
    setAlerts([
      ...alerts,
      { ...form, id: Date.now(), enabled: true },
    ]);
    setShowForm(false);
    setForm({ fund_code: "", alert_type: "price_cross", threshold: 0, direction: "above" });
  };

  const handleDelete = (id: number) => {
    setAlerts(alerts.filter((a) => a.id !== id));
  };

  const handleToggle = (id: number) => {
    setAlerts(
      alerts.map((a) => (a.id === id ? { ...a, enabled: !a.enabled } : a))
    );
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-orange-500/10">
            <RiNotification3Line className="w-6 h-6 text-orange-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">告警中心</h1>
            <p className="text-sm text-gray-400 mt-0.5">配置价格、涨跌幅等多维预警规则</p>
          </div>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2.5 bg-orange-500 hover:bg-orange-600 text-white text-sm rounded-xl transition-all"
        >
          <RiAddLine className="w-4 h-4" />
          新建告警
        </button>
      </div>

      {/* 新建表单 */}
      {showForm && (
        <div className="glass-card p-5 space-y-3">
          <h3 className="font-medium">新建告警规则</h3>
          <div className="grid grid-cols-4 gap-3">
            <input
              placeholder="基金代码 *"
              value={form.fund_code}
              onChange={(e) => setForm({ ...form, fund_code: e.target.value })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-orange-500/50"
            />
            <select
              value={form.alert_type}
              onChange={(e) => setForm({ ...form, alert_type: e.target.value })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 focus:outline-none focus:border-orange-500/50"
            >
              {Object.entries(alertTypes).map(([value, label]) => (
                <option key={value} value={value} className="bg-gray-800">
                  {label}
                </option>
              ))}
            </select>
            <input
              type="number"
              placeholder="阈值 *"
              value={form.threshold || ""}
              onChange={(e) => setForm({ ...form, threshold: Number(e.target.value) })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-orange-500/50"
            />
            <select
              value={form.direction}
              onChange={(e) => setForm({ ...form, direction: e.target.value })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 focus:outline-none focus:border-orange-500/50"
            >
              <option value="above" className="bg-gray-800">突破上方</option>
              <option value="below" className="bg-gray-800">跌破下方</option>
              <option value="up" className="bg-gray-800">上涨</option>
              <option value="down" className="bg-gray-800">下跌</option>
            </select>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleAdd}
              className="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white text-sm rounded-lg transition-all"
            >
              确认创建
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="px-4 py-2 border border-white/10 text-gray-400 text-sm rounded-lg hover:text-gray-200 transition-all"
            >
              取消
            </button>
          </div>
        </div>
      )}

      {/* 告警列表 */}
      <div className="space-y-2">
        {alerts.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <RiNotification3Line className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-500">还没有告警规则</p>
            <p className="text-sm text-gray-600 mt-1">创建告警，市场变动时第一时间收到通知</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="glass-card p-4 flex items-center justify-between"
            >
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-lg bg-orange-500/10 flex items-center justify-center">
                  <RiNotification3Line className="w-5 h-5 text-orange-400" />
                </div>
                <div>
                  <div className="font-medium">
                    {alert.fund_code} - {alertTypes[alert.alert_type]}
                  </div>
                  <div className="text-xs text-gray-500">
                    阈值: {alert.threshold} | 方向: {alert.direction}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => handleToggle(alert.id)}
                  className={`p-1 rounded-lg transition-colors ${
                    alert.enabled ? "text-orange-400" : "text-gray-600"
                  }`}
                >
                  {alert.enabled ? (
                    <RiToggleFill className="w-6 h-6" />
                  ) : (
                    <RiToggleLine className="w-6 h-6" />
                  )}
                </button>
                <button
                  onClick={() => handleDelete(alert.id)}
                  className="p-1.5 text-gray-500 hover:text-red-400 rounded-lg transition-colors"
                >
                  <RiDeleteBin6Line className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
