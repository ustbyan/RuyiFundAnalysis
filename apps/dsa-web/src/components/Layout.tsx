import { useState } from "react";
import { Outlet, NavLink, useLocation } from "react-router-dom";
import {
  RiHome4Line,
  RiRobot2Line,
  RiStarLine,
  RiBriefcase4Line,
  RiLineChartLine,
  RiNotification3Line,
  RiBarChartBoxLine,
  RiSettings3Line,
  RiMenuFoldLine,
  RiMenuUnfoldLine,
  RiFundsLine,
} from "@remixicon/react";

const navItems = [
  { path: "/", label: "智能分析", icon: RiHome4Line },
  { path: "/ai-qa", label: "AI 问基", icon: RiRobot2Line },
  { path: "/watchlist", label: "自选管理", icon: RiStarLine },
  { path: "/portfolio", label: "持仓管理", icon: RiBriefcase4Line },
  { path: "/backtest", label: "回测分析", icon: RiLineChartLine },
  { path: "/alerts", label: "告警中心", icon: RiNotification3Line },
  { path: "/usage", label: "用量监控", icon: RiBarChartBoxLine },
  { path: "/settings", label: "系统设置", icon: RiSettings3Line },
];

export default function Layout() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  return (
    <div className="flex h-screen bg-gray-950 text-gray-100">
      {/* 左侧导航 */}
      <aside
        className={`flex flex-col glass border-r border-white/5 transition-all duration-300 ${
          collapsed ? "w-16" : "w-56"
        }`}
      >
        {/* Logo */}
        <div className="flex items-center h-16 px-4 border-b border-white/5">
          <RiFundsLine className="w-7 h-7 text-blue-400 flex-shrink-0" />
          {!collapsed && (
            <span className="ml-3 text-lg font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent whitespace-nowrap">
              如意基金分析
            </span>
          )}
        </div>

        {/* 导航菜单 */}
        <nav className="flex-1 py-4 px-2 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive =
              item.path === "/"
                ? location.pathname === "/"
                : location.pathname.startsWith(item.path);
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 group ${
                  isActive
                    ? "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                    : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
                }`}
                title={collapsed ? item.label : undefined}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {!collapsed && <span>{item.label}</span>}
              </NavLink>
            );
          })}
        </nav>

        {/* 折叠按钮 */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center justify-center h-12 border-t border-white/5 text-gray-500 hover:text-gray-300 transition-colors"
        >
          {collapsed ? (
            <RiMenuUnfoldLine className="w-5 h-5" />
          ) : (
            <RiMenuFoldLine className="w-5 h-5" />
          )}
        </button>
      </aside>

      {/* 右侧内容区 */}
      <main className="flex-1 overflow-auto">
        <div className="p-6 max-w-7xl mx-auto animate-fade-in">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
