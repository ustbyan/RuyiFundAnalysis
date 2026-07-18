import { useState, useEffect } from "react";
import { RiBriefcase4Line, RiAddLine, RiUploadLine } from "@remixicon/react";
import { getPortfolio, updatePortfolio } from "@/utils/api";
import { motion } from "motion/react";

interface PortfolioItem {
  id: number;
  fund_code: string;
  fund_name: string;
  shares: number;
  cost_price: number;
  current_price: number;
  market_value: number;
  profit_loss: number;
  profit_loss_pct: number;
}

export default function Portfolio() {
  const [items, setItems] = useState<PortfolioItem[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    fund_code: "",
    fund_name: "",
    shares: 0,
    cost_price: 0,
  });

  const loadPortfolio = async () => {
    try {
      const res = await getPortfolio();
      setItems(res.data.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadPortfolio();
  }, []);

  const handleSubmit = async () => {
    if (!form.fund_code || form.shares <= 0) return;
    try {
      await updatePortfolio(form);
      setShowForm(false);
      setForm({ fund_code: "", fund_name: "", shares: 0, cost_price: 0 });
      loadPortfolio();
    } catch (err) {
      console.error(err);
    }
  };

  const totalValue = items.reduce((sum, item) => sum + (item.market_value || 0), 0);
  const totalPL = items.reduce((sum, item) => sum + (item.profit_loss || 0), 0);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-emerald-500/10">
            <RiBriefcase4Line className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">持仓管理</h1>
            <p className="text-sm text-gray-400 mt-0.5">跟踪你的基金持仓和收益</p>
          </div>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white text-sm rounded-xl transition-all"
        >
          <RiAddLine className="w-4 h-4" />
          添加持仓
        </button>
      </div>

      {/* 汇总卡片 */}
      {items.length > 0 && (
        <div className="grid grid-cols-3 gap-4">
          <div className="glass-card p-4">
            <div className="text-xs text-gray-500">总市值</div>
            <div className="text-2xl font-bold text-gray-100 mt-1">
              ¥{totalValue.toLocaleString()}
            </div>
          </div>
          <div className="glass-card p-4">
            <div className="text-xs text-gray-500">持仓盈亏</div>
            <div
              className={`text-2xl font-bold mt-1 ${
                totalPL >= 0 ? "text-red-400" : "text-green-400"
              }`}
            >
              {totalPL >= 0 ? "+" : ""}¥{totalPL.toLocaleString()}
            </div>
          </div>
          <div className="glass-card p-4">
            <div className="text-xs text-gray-500">持仓数量</div>
            <div className="text-2xl font-bold text-gray-100 mt-1">{items.length} 只</div>
          </div>
        </div>
      )}

      {/* 添加表单 */}
      {showForm && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-5 space-y-3"
        >
          <h3 className="font-medium">添加持仓</h3>
          <div className="grid grid-cols-2 gap-3">
            <input
              placeholder="基金代码 *"
              value={form.fund_code}
              onChange={(e) => setForm({ ...form, fund_code: e.target.value })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-emerald-500/50"
            />
            <input
              placeholder="基金名称"
              value={form.fund_name}
              onChange={(e) => setForm({ ...form, fund_name: e.target.value })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-emerald-500/50"
            />
            <input
              type="number"
              placeholder="持有份额 *"
              value={form.shares || ""}
              onChange={(e) => setForm({ ...form, shares: Number(e.target.value) })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-emerald-500/50"
            />
            <input
              type="number"
              placeholder="成本价格 *"
              value={form.cost_price || ""}
              onChange={(e) => setForm({ ...form, cost_price: Number(e.target.value) })}
              className="px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-emerald-500/50"
            />
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleSubmit}
              className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white text-sm rounded-lg transition-all"
            >
              确认添加
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="px-4 py-2 border border-white/10 text-gray-400 text-sm rounded-lg hover:text-gray-200 transition-all"
            >
              取消
            </button>
          </div>
        </motion.div>
      )}

      {/* 持仓列表 */}
      <div className="space-y-2">
        {items.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <RiBriefcase4Line className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-500">还没有持仓记录</p>
            <p className="text-sm text-gray-600 mt-1">点击"添加持仓"开始记录</p>
          </div>
        ) : (
          items.map((item) => (
            <div
              key={item.id}
              className="glass-card p-4 flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400 text-sm font-bold">
                  {item.fund_code.slice(0, 2)}
                </div>
                <div>
                  <div className="font-medium">{item.fund_name || item.fund_code}</div>
                  <div className="text-xs text-gray-500">
                    {item.shares.toLocaleString()} 份 · 成本 ¥{item.cost_price}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-medium">¥{(item.market_value || 0).toLocaleString()}</div>
                <div
                  className={`text-xs ${
                    (item.profit_loss_pct || 0) >= 0
                      ? "text-red-400"
                      : "text-green-400"
                  }`}
                >
                  {(item.profit_loss_pct || 0) >= 0 ? "+" : ""}
                  {item.profit_loss_pct?.toFixed(2) || "0.00"}%
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
