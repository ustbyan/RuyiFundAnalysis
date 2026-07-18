import { useState, useRef, useEffect } from "react";
import { RiRobot2Line, RiSendPlaneFill, RiUser3Line } from "@remixicon/react";
import { analyzeFund } from "@/utils/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  role: "user" | "assistant";
  content: string;
  data?: any;
}

export default function AIQA() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "你好！我是如意 AI 基金助手 🏮\n\n我可以帮你：\n- 📊 分析基金（如"帮我分析 510050"）\n- 📈 解读净值走势\n- 🔍 搜索基金信息\n- 💡 回答投资相关问题\n\n请告诉我你想了解什么？",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // 检测是否是分析基金请求
      const fundCodeMatch = input.match(/(\d{6})/);
      let reply = "";

      if (fundCodeMatch && input.includes("分析")) {
        const code = fundCodeMatch[1];
        const res = await analyzeFund(code);
        const data = res.data.data;

        reply = `## 📊 ${data.fund_name || code} 分析结果\n\n`;
        reply += `**综合评分**: ${data.overall_score}/100\n`;
        reply += `**评级**: ${data.rating || "N/A"}\n\n`;
        if (data.ai_analysis?.summary) {
          reply += `${data.ai_analysis.summary}\n\n`;
        }
        if (data.ai_analysis?.advice) {
          reply += `> 💡 ${data.ai_analysis.advice}`;
        }
      } else {
        // 模拟 AI 对话（实际可接入 LLM Agent）
        reply = generateMockReply(input);
      }

      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `抱歉，出了点问题：${err.message || "未知错误"}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      {/* 标题 */}
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-xl bg-purple-500/10">
          <RiRobot2Line className="w-6 h-6 text-purple-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold">AI 问基</h1>
          <p className="text-sm text-gray-400 mt-0.5">对话式基金智能问答</p>
        </div>
      </div>

      {/* 对话区域 */}
      <div className="flex-1 glass-card p-4 mb-4 overflow-y-auto space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`}
          >
            {msg.role === "assistant" && (
              <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center flex-shrink-0">
                <RiRobot2Line className="w-4 h-4 text-purple-400" />
              </div>
            )}
            <div
              className={`max-w-[80%] px-4 py-3 rounded-2xl ${
                msg.role === "user"
                  ? "bg-blue-500/20 border border-blue-500/20"
                  : "bg-white/5 border border-white/5"
              }`}
            >
              <div className="prose prose-invert prose-sm max-w-none">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {msg.content}
                </ReactMarkdown>
              </div>
            </div>
            {msg.role === "user" && (
              <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                <RiUser3Line className="w-4 h-4 text-blue-400" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center flex-shrink-0">
              <RiRobot2Line className="w-4 h-4 text-purple-400" />
            </div>
            <div className="px-4 py-3 rounded-2xl bg-white/5 border border-white/5">
              <div className="flex gap-1.5">
                <span className="w-2 h-2 rounded-full bg-purple-400 animate-bounce" />
                <span className="w-2 h-2 rounded-full bg-purple-400 animate-bounce [animation-delay:0.1s]" />
                <span className="w-2 h-2 rounded-full bg-purple-400 animate-bounce [animation-delay:0.2s]" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* 输入栏 */}
      <div className="glass-card p-3 flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
          placeholder="输入基金代码或问题..."
          className="flex-1 px-4 py-2.5 bg-transparent border-none outline-none text-gray-100 placeholder-gray-500"
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || loading}
          className="px-4 py-2.5 bg-purple-500 hover:bg-purple-600 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-xl transition-all disabled:cursor-not-allowed"
        >
          <RiSendPlaneFill className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}

function generateMockReply(input: string): string {
  const lowered = input.toLowerCase();

  if (lowered.includes("什么是") || lowered.includes("介绍")) {
    return "基金是一种集合投资工具，由基金公司发行，汇集众多投资者的资金，由专业的基金经理进行投资管理。\n\n常见基金类型包括：\n- **ETF（交易型开放式指数基金）**：可在交易所买卖，跟踪特定指数\n- **股票型基金**：主要投资股票，风险和收益较高\n- **混合型基金**：同时投资股票和债券\n- **债券型基金**：主要投资债券，风险较低\n- **货币基金**：投资短期货币市场工具，流动性好";
  }

  if (lowered.includes("推荐") || lowered.includes("选")) {
    return "选择基金需要综合考虑多个因素：\n\n1. **投资目标**：确定你的风险偏好和收益预期\n2. **基金类型**：ETF、指数、主动管理各有优劣\n3. **历史业绩**：关注长期表现而非短期\n4. **费率**：低费率长期能省不少钱\n5. **基金经理**：主动管理基金要看经理历史\n\n你可以告诉我具体的基金代码，我帮你详细分析！";
  }

  if (lowered.includes("定投") || lowered.includes("定投策略")) {
    return "基金定投（定期定额投资）是一种适合普通投资者的策略：\n\n**优势**：\n- 📉 摊平成本，降低择时风险\n- 🕐 省心省力，无需盯盘\n- 💰 强制储蓄，积少成多\n\n**适合定投的基金**：\n- 宽基指数 ETF（如沪深300、中证500）\n- 行业 ETF（长期看好赛道）\n- 主动管理优质基金\n\n**建议**：坚持长期定投，市场低迷时不要停止。";
  }

  return "这是一个好问题！不过作为基金分析助手，我建议你可以尝试：\n\n- 直接输入基金代码让我分析（如 510050）\n- 询问具体的投资问题\n- 让我帮你查看自选基金的表现\n\n你想了解什么呢？🏮";
}
