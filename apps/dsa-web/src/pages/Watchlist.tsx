import { useState, useEffect } from "react";
import { RiStarLine, RiAddLine, RiDeleteBin6Line, RiSearchLine, RiFlashlightLine } from "@remixicon/react";
import { getWatchlist, addToWatchlist, removeFromWatchlist, searchFunds, analyzeFund } from "@/utils/api";
import { motion } from "motion/react";

interface WatchlistItem {
  id: number;
  fund_code: string;
  fund_name: string;
  fund_type: string;
  group_name: string;
}

export default function Watchlist() {
  const [items, setItems] = useState<WatchlistItem[]>([]);
  const [searchKeyword, setSearchKeyword] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [showSearch, setShowSearch] = useState(false);
  const [analyzing, setAnalyzing] = useState<string | null>(null);

  const loadWatchlist = async () => {
    try {
      const res = await getWatchlist();
      setItems(res.data.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadWatchlist();
  }, []);

  const handleSearch = async () => {
    if (!searchKeyword.trim()) return;
    try {
      const res = await searchFunds(searchKeyword.trim());
      setSearchResults(res.data.data || []);
      setShowSearch(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAdd = async (code: string, name: string, type: string) => {
    try {
      await addToWatchlist({ fund_code: code, fund_name: name, fund_type: type });
      setShowSearch(false);
      setSearchKeyword("");
      loadWatchlist();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemove = async (code: string) => {
    try {
      await removeFromWatchlist(code);
      loadWatchlist();
    } catch (err) {
      console.error(err);
    }
  };

  const handleQuickAnalyze = async (code: string) => {
    setAnalyzing(code);
    try {
      await analyzeFund(code);
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(null);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-yellow-500/10">
          <RiStarLine className="w-6 h-6 text-yellow-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold">自选管理</h1>
          <p className="text-sm text-gray-400 mt-0.5">管理你的基金关注列表</p>
        </div>
      </div>

      {/* 搜索添加 */}
      <div className="glass-card p-4">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <RiSearchLine className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input
              type="text"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              placeholder="搜索基金代码或名称..."
              className="w-full pl-9 pr-4 py-2.5 bg-white/5 border border-white/10 rounded-lg text-gray-100 text-sm placeholder-gray-500 focus:outline-none focus:border-blue-500/50"
            />
          </div>
          <button
            onClick={handleSearch}
            className="px-4 py-2.5 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded-lg transition-all"
          >
            搜索
          </button>
        </div>

        {showSearch && searchResults.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-3 space-y-1"
          >
            {searchResults.map((fund) => (
              <div
                key={fund.code}
                className="flex items-center justify-between p-3 rounded-lg bg-white/5 border border-white/5 hover:border-blue-500/20 transition-all"
              >
                <div>
                  <span className="text-sm font-medium">{fund.name}</span>
                  <span className="text-xs text-gray-500 ml-2">{fund.code}</span>
                  {fund.type && (
                    <span className="text-xs text-gray-500 ml-2">({fund.type})</span>
                  )}
                </div>
                <button
                  onClick={() => handleAdd(fund.code, fund.name, fund.type)}
                  className="flex items-center gap-1 px-3 py-1.5 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 text-xs rounded-lg transition-all"
                >
                  <RiAddLine className="w-3.5 h-3.5" />
                  添加
                </button>
              </div>
            ))}
          </motion.div>
        )}
      </div>

      {/* 自选列表 */}
      <div className="space-y-2">
        {items.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <RiStarLine className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-500">还没有添加自选基金</p>
            <p className="text-sm text-gray-600 mt-1">搜索并添加你关注的基金</p>
          </div>
        ) : (
          items.map((item) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="glass-card p-4 flex items-center justify-between group"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-yellow-500/10 flex items-center justify-center">
                  <RiStarLine className="w-5 h-5 text-yellow-400" />
                </div>
                <div>
                  <div className="font-medium">{item.fund_name || item.fund_code}</div>
                  <div className="text-xs text-gray-500">
                    {item.fund_code} {item.fund_type && `· ${item.fund_type}`}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={() => handleQuickAnalyze(item.fund_code)}
                  disabled={analyzing === item.fund_code}
                  className="flex items-center gap-1 px-3 py-1.5 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 text-xs rounded-lg transition-all"
                >
                  <RiFlashlightLine className="w-3 h-3" />
                  {analyzing === item.fund_code ? "分析中..." : "分析"}
                </button>
                <button
                  onClick={() => handleRemove(item.fund_code)}
                  className="p-1.5 text-gray-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all"
                >
                  <RiDeleteBin6Line className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}
