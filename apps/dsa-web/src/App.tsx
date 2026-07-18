import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import AIQA from "./pages/AIQA";
import Watchlist from "./pages/Watchlist";
import Portfolio from "./pages/Portfolio";
import Backtest from "./pages/Backtest";
import Alerts from "./pages/Alerts";
import Usage from "./pages/Usage";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="ai-qa" element={<AIQA />} />
        <Route path="watchlist" element={<Watchlist />} />
        <Route path="portfolio" element={<Portfolio />} />
        <Route path="backtest" element={<Backtest />} />
        <Route path="alerts" element={<Alerts />} />
        <Route path="usage" element={<Usage />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
