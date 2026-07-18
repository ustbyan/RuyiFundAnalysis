import { useState, useEffect } from "react";
import {
  RiSettings3Line,
  RiCheckLine,
  RiCloseLine,
  RiAlertLine,
} from "@remixicon/react";
import { getSettings, checkConnection } from "@/utils/api";

export default function Settings() {
  const [settings, setSettings] = useState<any>({});
  const [connectionChecks, setConnectionChecks] = useState<any>({});
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const res = await getSettings();
      setSettings(res.data.data || {});
    } catch (err) {
      console.error(err);
    }
  };

  const handleCheckConnection = async () => {
    try {
      const res = await checkConnection();
      setConnectionChecks(res.data.data || {});
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-gray-500/10">
          <RiSettings3Line className="w-6 h-6 text-gray-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold">系统设置</h1>
          <p className="text-sm text-gray-400 mt-0.5">配置 LLM 通道、自选股列表、通知渠道</p>
        </div>
      </div>

      {/* LLM 配置 */}
      <div className="glass-card p-5">
        <h3 className="font-medium mb-4 flex items-center gap-2">
          <span className="w-1 h-4 rounded-full bg-blue-500" />
          LLM 模型配置
        </h3>
        <div className="space-y-3">
          <div>
            <label className="text-xs text-gray-500 mb-1 block">主模型</label>
            <input
              type="text"
              defaultValue={settings.llm_model || ""}
              placeholder="deepseek/deepseek-chat"
              className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500/50"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-gray-500 mb-1 block">DeepSeek API Key</label>
              <input
                type="password"
                placeholder="sk-..."
                className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500/50"
              />
            </div>
            <div>
              <label className="text-xs text-gray-500 mb-1 block">Gemini API Key</label>
              <input
                type="password"
                placeholder="AIza..."
                className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500/50"
              />
            </div>
          </div>
        </div>

        {/* 连通性检查 */}
        <div className="mt-4 pt-4 border-t border-white/5">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-400">连通性检查</span>
            <button
              onClick={handleCheckConnection}
              className="px-3 py-1.5 bg-white/5 hover:bg-white/10 text-sm text-gray-300 rounded-lg transition-all"
            >
              检查
            </button>
          </div>
          {Object.keys(connectionChecks).length > 0 && (
            <div className="mt-3 space-y-1.5">
              {Object.entries(connectionChecks).map(([name, info]: [string, any]) => (
                <div
                  key={name}
                  className="flex items-center justify-between p-2 rounded-lg bg-white/5 text-sm"
                >
                  <span className="text-gray-400 capitalize">{name}</span>
                  <div className="flex items-center gap-1.5">
                    {info.configured ? (
                      <>
                        <RiCheckLine className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 text-xs">{info.status}</span>
                      </>
                    ) : (
                      <>
                        <RiCloseLine className="w-4 h-4 text-gray-600" />
                        <span className="text-gray-600 text-xs">{info.status}</span>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 自选基金列表 */}
      <div className="glass-card p-5">
        <h3 className="font-medium mb-4 flex items-center gap-2">
          <span className="w-1 h-4 rounded-full bg-yellow-500" />
          自选基金列表
        </h3>
        <textarea
          defaultValue={settings.fund_list || ""}
          placeholder="510050,510300,159915,000011"
          rows={2}
          className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-yellow-500/50 resize-none"
        />
        <p className="text-xs text-gray-600 mt-1.5">逗号分隔，场内ETF和场外基金均支持</p>
      </div>

      {/* 通知渠道 */}
      <div className="glass-card p-5">
        <h3 className="font-medium mb-4 flex items-center gap-2">
          <span className="w-1 h-4 rounded-full bg-green-500" />
          通知渠道
        </h3>
        <div className="space-y-3">
          <div>
            <label className="text-xs text-gray-500 mb-1 block">企业微信 Webhook</label>
            <input
              type="text"
              placeholder="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..."
              className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-green-500/50"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 mb-1 block">飞书 Webhook</label>
            <input
              type="text"
              placeholder="https://open.feishu.cn/open-apis/bot/v2/hook/..."
              className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-green-500/50"
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 mb-1 block">钉钉 Webhook</label>
            <input
              type="text"
              placeholder="https://oapi.dingtalk.com/robot/send?access_token=..."
              className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-green-500/50"
            />
          </div>
        </div>
      </div>

      {/* 分析配置 */}
      <div className="glass-card p-5">
        <h3 className="font-medium mb-4 flex items-center gap-2">
          <span className="w-1 h-4 rounded-full bg-purple-500" />
          分析配置
        </h3>
        <div className="grid grid-cols-3 gap-3">
          <div>
            <label className="text-xs text-gray-500 mb-1 block">报告语言</label>
            <select className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 focus:outline-none focus:border-purple-500/50">
              <option value="zh" className="bg-gray-800">中文</option>
              <option value="en" className="bg-gray-800">English</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-gray-500 mb-1 block">报告类型</label>
            <select className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 focus:outline-none focus:border-purple-500/50">
              <option value="simple" className="bg-gray-800">精简</option>
              <option value="full" className="bg-gray-800">完整</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-gray-500 mb-1 block">定时执行时间</label>
            <input
              type="time"
              defaultValue="18:00"
              className="w-full px-3 py-2.5 bg-white/5 border border-white/10 rounded-lg text-sm text-gray-100 focus:outline-none focus:border-purple-500/50"
            />
          </div>
        </div>

        <div className="flex items-center gap-3 mt-4">
          <label className="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
            <input type="checkbox" className="rounded accent-blue-500" />
            启用定时分析
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
            <input type="checkbox" className="rounded accent-blue-500" defaultChecked />
            启用大盘复盘
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
            <input type="checkbox" className="rounded accent-blue-500" />
            启用通知推送
          </label>
        </div>
      </div>

      {/* 保存按钮 */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          className="flex items-center gap-2 px-6 py-2.5 bg-blue-500 hover:bg-blue-600 text-white rounded-xl transition-all"
        >
          {saved ? (
            <>
              <RiCheckLine className="w-4 h-4" />
              已保存
            </>
          ) : (
            "保存设置"
          )}
        </button>
      </div>
    </div>
  );
}
