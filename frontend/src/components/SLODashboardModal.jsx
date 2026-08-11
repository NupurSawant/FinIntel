import React, { useState, useEffect } from "react";
import {
  X,
  Info,
  Activity,
  Clock,
  Zap,
  CheckCircle2,
  AlertTriangle,
  ShieldAlert,
  Cpu,
  DollarSign,
  Layers,
  TrendingUp,
  RefreshCw,
  Gauge,
  RotateCcw,
} from "lucide-react";
import { getSLOMetrics, resetSLOMetrics } from "../api";

const METRIC_DESCRIPTIONS = {
  end_to_end_response_time:
    "Total latency (in seconds) measured from the moment a user submits a query to the exact millisecond the final answer is rendered.",
  ollama_routing_time:
    "Latency of the Ollama Llama 3.2 pre-classifier step that evaluates whether a query is simple conversational vs. complex financial.",
  individual_agent_latency:
    "Execution time breakdown (in seconds) spent inside each individual multi-agent node: Manager, Risk, Market, SQL, RAG, and Critic.",
  critic_revision_rate:
    "Percentage of queries that failed initial critic review and required one or more feedback revision loops to improve accuracy.",
  confidence_score_distribution:
    "Average confidence score (0.0 to 1.0) assigned by the Critic Agent based on factual grounding, math correctness, and attribution.",
  routing_accuracy:
    "Ratio of user queries correctly classified and routed to direct execution vs. full multi-agent crew orchestration.",
  rag_retrieval_success:
    "Percentage of document RAG vector searches that successfully returned top-k relevant context chunks without error.",
  sql_success_rate:
    "Percentage of generated database queries that executed cleanly against PostgreSQL / SQLite without syntax or schema errors.",
  market_api_success:
    "Success rate of real-time financial market data API fetches from Tavily Search & Yahoo Finance services.",
  guardrail_blocks:
    "Total count of queries intercepted and rejected by safety guardrails (length limit, SQL injection, PII, out-of-domain, etc.).",
  human_handoff_rate:
    "Percentage of complex queries escalated to human review (sawant.nupur25@gmail.com) when confidence threshold wasn't met after max retries.",
  error_rate:
    "Percentage of total API calls resulting in unhandled backend exceptions, 500 errors, or network connection timeouts.",
  cost_savings:
    "Estimated total cost ($) saved by bypassing cloud LLM calls for simple queries using local Ollama Llama 3.2 pre-routing.",
  average_tokens:
    "Average prompt plus completion token consumption per user query across all agent processing steps.",
};

export default function SLODashboardModal({ isOpen, onClose, token, username }) {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [resetting, setResetting] = useState(false);
  const [activeTooltip, setActiveTooltip] = useState(null);
  const [lastRefreshed, setLastRefreshed] = useState("");

  const fetchMetrics = async () => {
    setLoading(true);
    const data = await getSLOMetrics(token, username);
    if (data) {
      setMetrics(data);
      setLastRefreshed(new Date().toLocaleTimeString());
    }
    setLoading(false);
  };

  const handleResetMetrics = async () => {
    if (!window.confirm("Are you sure you want to reset all SLO metrics back to zero?")) return;
    setResetting(true);
    setMetrics({
      end_to_end_response_time: 0.0,
      ollama_routing_time: 0.0,
      individual_agent_latency: {
        Manager: 0.0,
        Risk: 0.0,
        Market: 0.0,
        SQL: 0.0,
        RAG: 0.0,
        Critic: 0.0,
      },
      critic_revision_rate: 0.0,
      confidence_score_distribution: 0.0,
      routing_accuracy: 100.0,
      rag_retrieval_success: 100.0,
      sql_success_rate: 100.0,
      market_api_success: 100.0,
      guardrail_blocks: 0,
      human_handoff_rate: 0.0,
      error_rate: 0.0,
      cost_savings: 0.0,
      average_tokens: 0,
      total_queries_processed: 0,
    });
    setLastRefreshed(new Date().toLocaleTimeString());
    await resetSLOMetrics(token, username);
    await fetchMetrics();
    setResetting(false);
  };

  useEffect(() => {
    if (!isOpen) return;
    fetchMetrics();

    const handleKeyDown = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-950/85 backdrop-blur-md p-4 overflow-hidden select-none animate-fade-in"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="w-full max-w-5xl max-h-[85vh] my-auto bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col relative text-slate-100">
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/80 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-blue-500/10 border border-blue-500/20 text-[#2563EB]">
              <Gauge className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100 tracking-tight flex items-center gap-2">
                SLO &amp; System Metrics Dashboard
              </h2>
              <p className="text-xs text-slate-400">
                Real-time Service Level Objectives, Latency, Accuracy &amp; Efficiency
                {lastRefreshed && <span className="ml-2 text-emerald-400">• Updated {lastRefreshed}</span>}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchMetrics}
              title="Refresh Metrics"
              disabled={loading || resetting}
              className="px-3 py-1.5 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl transition text-xs font-medium flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-[#2563EB]" : ""}`} />
              <span className="hidden sm:inline">Refresh</span>
            </button>
            <button
              onClick={handleResetMetrics}
              title="Reset all SLO metrics back to zero"
              disabled={loading || resetting}
              className="px-3 py-1.5 text-rose-300 hover:text-white bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 rounded-xl transition text-xs font-medium flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
            >
              <RotateCcw className={`w-3.5 h-3.5 ${resetting ? "animate-spin text-rose-400" : ""}`} />
              <span>Reset</span>
            </button>
            <button
              onClick={onClose}
              title="Close SLO Dashboard (Esc)"
              className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-red-500/20 hover:text-red-400 border border-slate-700 text-slate-200 text-xs font-bold flex items-center gap-1.5 transition active:scale-95 shadow"
            >
              <X className="w-4 h-4" />
              <span>Close</span>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading && !metrics ? (
            <div className="py-20 text-center text-slate-400 flex flex-col items-center gap-3">
              <RefreshCw className="w-6 h-6 animate-spin text-[#2563EB]" />
              <span className="text-sm font-medium">Loading real-time SLO metrics...</span>
            </div>
          ) : (
            <>
              {/* Category 1: Latency & Response Times */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                  <Clock className="w-4 h-4 text-blue-400" />
                  Latency &amp; Response Time SLOs
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* End-to-End Response Time */}
                  <MetricCard
                    title="End-to-End Response Time"
                    value={`${metrics?.end_to_end_response_time ?? 0}s`}
                    metricKey="end_to_end_response_time"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-blue-400"
                    badge="Target < 5.0s"
                  />

                  {/* Ollama Routing Time */}
                  <MetricCard
                    title="Ollama Routing Time"
                    value={`${metrics?.ollama_routing_time ?? 0}s`}
                    metricKey="ollama_routing_time"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-indigo-400"
                    badge="Target < 0.5s"
                  />

                  {/* Cost Savings */}
                  <MetricCard
                    title="Cost Savings"
                    value={`$${metrics?.cost_savings ?? 0}`}
                    metricKey="cost_savings"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-emerald-400"
                    badge="Local Routing"
                  />
                </div>
              </div>

              {/* Individual Agent Latency Breakdown */}
              <div className="bg-slate-950/60 border border-slate-800/80 rounded-2xl p-4">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
                    <Cpu className="w-4 h-4 text-purple-400" />
                    Individual Agent Latencies
                  </h4>
                  <InfoButton
                    metricKey="individual_agent_latency"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                  />
                </div>
                {activeTooltip === "individual_agent_latency" && (
                  <div className="mb-3 p-3 rounded-xl bg-slate-800/90 border border-slate-700 text-xs text-slate-300 leading-relaxed animate-fade-in">
                    {METRIC_DESCRIPTIONS.individual_agent_latency}
                  </div>
                )}
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
                  {Object.entries(
                    metrics?.individual_agent_latency || {
                      Manager: 0,
                      Risk: 0,
                      Market: 0,
                      SQL: 0,
                      RAG: 0,
                      Critic: 0,
                    }
                  ).map(([agent, lat]) => (
                    <div key={agent} className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl text-center">
                      <span className="text-[11px] font-semibold text-slate-400 block">{agent} Agent</span>
                      <span className="text-sm font-bold text-slate-100">{lat}s</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Category 2: Accuracy & Reliability SLOs */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  Accuracy &amp; Retrieval Reliability SLOs
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                  {/* Critic Revision Rate */}
                  <MetricCard
                    title="Critic Revision Rate"
                    value={`${metrics?.critic_revision_rate ?? 0}%`}
                    metricKey="critic_revision_rate"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-amber-400"
                    badge="Target < 20%"
                  />

                  {/* Confidence Score Distribution */}
                  <MetricCard
                    title="Confidence Score Dist."
                    value={`${metrics?.confidence_score_distribution ?? 0} / 1.0`}
                    metricKey="confidence_score_distribution"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-emerald-400"
                    badge="Avg Confidence"
                  />

                  {/* Routing Accuracy */}
                  <MetricCard
                    title="Routing Accuracy"
                    value={`${metrics?.routing_accuracy ?? 100}%`}
                    metricKey="routing_accuracy"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-blue-400"
                    badge="Classifiers"
                  />

                  {/* RAG Retrieval Success */}
                  <MetricCard
                    title="RAG Retrieval Success"
                    value={`${metrics?.rag_retrieval_success ?? 100}%`}
                    metricKey="rag_retrieval_success"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-cyan-400"
                    badge="Target > 95%"
                  />
                </div>
              </div>

              {/* Category 3: Integration & System Operations */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                  <Layers className="w-4 h-4 text-purple-400" />
                  Integrations &amp; Operational SLOs
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                  {/* SQL Success Rate */}
                  <MetricCard
                    title="SQL Success Rate"
                    value={`${metrics?.sql_success_rate ?? 100}%`}
                    metricKey="sql_success_rate"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-emerald-400"
                    badge="Target 100%"
                  />

                  {/* Market API Success */}
                  <MetricCard
                    title="Market API Success"
                    value={`${metrics?.market_api_success ?? 100}%`}
                    metricKey="market_api_success"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-teal-400"
                    badge="External Data"
                  />

                  {/* Guardrail Blocks */}
                  <MetricCard
                    title="Guardrail Blocks"
                    value={`${metrics?.guardrail_blocks ?? 0} req`}
                    metricKey="guardrail_blocks"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-rose-400"
                    badge="Safety Rules"
                  />

                  {/* Human Handoff Rate */}
                  <MetricCard
                    title="Human Handoff Rate"
                    value={`${metrics?.human_handoff_rate ?? 0}%`}
                    metricKey="human_handoff_rate"
                    activeTooltip={activeTooltip}
                    setActiveTooltip={setActiveTooltip}
                    color="text-orange-400"
                    badge="Target < 5%"
                  />
                </div>
              </div>

              {/* Category 4: Error Rate & Tokens */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <MetricCard
                  title="Error Rate"
                  value={`${metrics?.error_rate ?? 0}%`}
                  metricKey="error_rate"
                  activeTooltip={activeTooltip}
                  setActiveTooltip={setActiveTooltip}
                  color="text-red-400"
                  badge="Target < 1.0%"
                />

                <MetricCard
                  title="Average Tokens Used"
                  value={`${metrics?.average_tokens ?? 0} tokens`}
                  metricKey="average_tokens"
                  activeTooltip={activeTooltip}
                  setActiveTooltip={setActiveTooltip}
                  color="text-purple-400"
                  badge="Per Request"
                />
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        <div className="p-3.5 px-6 border-t border-slate-800 flex items-center justify-between bg-slate-950/80 shrink-0 text-xs text-slate-400">
          <span>Click any ℹ️ icon to view detailed metric calculations and formulas.</span>
          <span className="text-[11px] text-slate-500"> </span>
        </div>
      </div>
    </div>
  );
}

function InfoButton({ metricKey, activeTooltip, setActiveTooltip }) {
  const isSelected = activeTooltip === metricKey;
  return (
    <button
      type="button"
      onClick={() => setActiveTooltip(isSelected ? null : metricKey)}
      title="Click to view metric description"
      className={`p-1 rounded-full transition ${isSelected
        ? "bg-[#2563EB] text-white"
        : "text-slate-500 hover:text-slate-200 hover:bg-slate-800"
        }`}
    >
      <Info className="w-3.5 h-3.5" />
    </button>
  );
}

function MetricCard({
  title,
  value,
  metricKey,
  activeTooltip,
  setActiveTooltip,
  color,
  badge,
}) {
  const showTooltip = activeTooltip === metricKey;

  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-2xl p-4 relative flex flex-col justify-between hover:border-slate-700 transition">
      <div>
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <span className="text-xs font-semibold text-slate-400 truncate">{title}</span>
          <div className="flex items-center gap-1">
            {badge && (
              <span className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-slate-900 border border-slate-800 text-slate-400">
                {badge}
              </span>
            )}
            <InfoButton
              metricKey={metricKey}
              activeTooltip={activeTooltip}
              setActiveTooltip={setActiveTooltip}
            />
          </div>
        </div>

        <div className={`text-xl font-extrabold ${color} tracking-tight`}>{value}</div>
      </div>

      {showTooltip && (
        <div className="mt-3 p-2.5 rounded-xl bg-slate-800/95 border border-slate-700 text-[11px] text-slate-200 leading-relaxed animate-fade-in z-10">
          {METRIC_DESCRIPTIONS[metricKey] || "Metric definition."}
        </div>
      )}
    </div>
  );
}
