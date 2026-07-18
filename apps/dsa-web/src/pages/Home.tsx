import { useState } from "react";
import { RiSearchLine, RiFlashlightLine, RiFundsLine, RiArrowUpLine, RiArrowDownLine } from "@remixicon/react";
import { analyzeFund, getMarketReview, type ApiResponse } from "@/utils/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { motion } from "motion/react";

export default function Home() {
  const [fundCode, setFundCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [marketReview, setMarketReview] = useState<any>(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!fundCode.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await analyzeFund(fundCode.trim());
      setResult(res.data.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "分析失败");
    } finally {
      setLoading(false);
    }
  };

  const handleMarketReview = async () => {
    try {
      const res = await getMarketReview();
      setMarketReview(res.data.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* 标题 */}
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-blue-500/10">
          <RiFlashlightLine className="w-6 h-6 text-blue-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold">智能分析</h1>
          <p className="text-sm text-gray-400 mt-0.5">输入基金代码，AI 综合研判</p>
        </div>
      </div>

      {/* 搜索栏 */}
      <div className="glass-card p-6">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <RiSearchLine className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              value={fundCode}
              onChange={(e) => setFundCode(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAnalyze()}
              placeholder="输入基金代码，如 510050、000011..."
              className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/30 transition-all"
            />
          </div>
          <button
            onClick={handleAnalyze}
            disabled={loading || !fundCode.trim()}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium rounded-xl transition-all flex items-center gap-2 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                分析中...
              </>
            ) : (
              <>
                <RiFlashlightLine className="w-4 h-4" />
                开始分析
              </>
            )}
          </button>

          <button
            onClick={handleMarketReview}
            className="px-4 py-3 border border-white/10 hover:border-blue-500/30 text-gray-300 hover:text-blue-400 rounded-xl transition-all flex items-center gap-2"
          >
            <RiFundsLine className="w-4 h-4" />
            大盘
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {error}
          </div>
        )}
      </div>

      {/* 大盘复盘 */}
      {marketReview && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-5"
        >
          <h3 className="text-sm font-medium text-gray-400 mb-3">市场环境</h3>
          <p className="text-gray-200">{marketReview.summary}</p>
          {marketReview.indices && (
            <div className="grid grid-cols-5 gap-3 mt-3">
              {Object.entries(marketReview.indices as Record<string, any>).map(([name, data]) => (
                <div
                  key={name}
                  className="p-3 rounded-lg bg-white/5 border border-white/5 text-center"
                >
                  <div className="text-xs text-gray-500">{name}</div>
                  <div className="text-lg font-semibold mt-1">
                    {data.close?.toFixed(0)}
                  </div>
                  <div
                    className={`text-xs mt-1 flex items-center justify-center gap-0.5 ${
                      data.change_pct > 0 ? "text-red-400" : "text-green-400"
                    }`}
                  >
                    {data.change_pct > 0 ? (
                      <RiArrowUpLine className="w-3 h-3" />
                    ) : (
                      <RiArrowDownLine className="w-3 h-3" />
                    )}
                    {data.change_pct > 0 ? "+" : ""}
                    {data.change_pct}%
                  </div>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {/* 分析结果 */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          {/* 总评卡片 */}
          <div className="glass-card p-6">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-xl font-bold">
                  {result.fund_name || result.fund_code}
                </h2>
                <p className="text-sm text-gray-400 mt-1">{result.fund_code}</p>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-400">
                    {result.overall_score}
                  </div>
                  <div className="text-xs text-gray-500">综合评分</div>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    result.rating?.includes("推荐")
                      ? "bg-green-500/10 text-green-400 border border-green-500/20"
                      : result.rating?.includes("中性")
                      ? "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20"
                      : "bg-gray-500/10 text-gray-400 border border-gray-500/20"
                  }`}
                >
                  {result.rating || "N/A"}
                </span>
              </div>
            </div>
          </div>

          {/* AI 分析 */}
          {result.ai_analysis && (
            <div className="glass-card p-6">
              <h3 className="text-sm font-medium text-gray-400 mb-4">
                AI 综合分析
              </h3>
              <div className="prose prose-invert prose-sm max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {result.ai_analysis.summary || "暂无分析摘要"}
                </ReactMarkdown>
              </div>

              {result.ai_analysis.key_points?.length > 0 && (
                <div className="mt-4 space-y-2">
                  {result.ai_analysis.key_points.map((point: string, i: number) => (
                    <div
                      key={i}
                      className="flex items-start gap-2 p-2 rounded-lg bg-blue-500/5 border border-blue-500/10"
                    >
                      <span className="text-blue-400 text-xs mt-0.5">●</span>
                      <span className="text-sm text-gray-300">{point}</span>
                    </div>
                  ))}
                </div>
              )}

              {result.ai_analysis.advice && (
                <div className="mt-4 p-3 rounded-lg bg-amber-500/5 border border-amber-500/10">
                  <div className="text-xs text-amber-400 mb-1">操作建议</div>
                  <div className="text-sm text-gray-200">{result.ai_analysis.advice}</div>
                </div>
              )}
            </div>
          )}

          {/* 评分明细 */}
          <div className="grid grid-cols-2 gap-4">
            {result.scores && (
              <>
                <div className="glass-card p-5">
                  <h4 className="text-xs text-gray-500 mb-2">技术面评分</h4>
                  <div className="text-2xl font-bold text-blue-400">
                    {result.scores.technical?.score || 0}/100
                  </div>
                  {result.scores.technical?.highlights?.length > 0 && (
                    <ul className="mt-2 space-y-1">
                      {result.scores.technical.highlights.map((h: string, i: number) => (
                        <li key={i} className="text-xs text-gray-400">✓ {h}</li>
                      ))}
                    </ul>
                  )}
                </div>
                <div className="glass-card p-5">
                  <h4 className="text-xs text-gray-500 mb-2">基本面评分</h4>
                  <div className="text-2xl font-bold text-cyan-400">
                    {result.scores.fundamental?.score || 0}/100
                  </div>
                  {result.scores.fundamental?.highlights?.length > 0 && (
                    <ul className="mt-2 space-y-1">
                      {result.scores.fundamental.highlights.map((h: string, i: number) => (
                        <li key={i} className="text-xs text-gray-400">✓ {h}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}
