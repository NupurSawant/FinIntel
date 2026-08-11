import React, { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Loader2,
  AlertTriangle,
  ShieldAlert,
  Search,
  Users,
  Database,
  FileText,
  AlertOctagon,
  CheckCircle2,
  Gauge,
} from "lucide-react";
import { Logo } from "./Logo";
import SLODashboardModal from "./SLODashboardModal";
import { sendQueryStream, createConversation, listConversations } from "../api";

// Multi-Agent Pipeline steps matching the UI mockup in Image 1
const AGENT_NODES = [
  { id: "query", label: "Query", icon: Search, color: "text-[#2563EB]", bg: "bg-[#2563EB]/10", border: "border-[#2563EB]" },
  { id: "crew_node", label: "Manager", icon: Users, color: "text-[#9333EA]", bg: "bg-[#9333EA]/10", border: "border-[#9333EA]" },
  { id: "sql_agent", label: "SQL Agent", icon: Database, color: "text-[#16A34A]", bg: "bg-[#16A34A]/10", border: "border-[#16A34A]" },
  { id: "rag_agent", label: "RAG Agent", icon: FileText, color: "text-[#EA580C]", bg: "bg-[#EA580C]/10", border: "border-[#EA580C]" },
  { id: "risk_agent", label: "Risk Agent", icon: AlertOctagon, color: "text-[#DC2626]", bg: "bg-[#DC2626]/10", border: "border-[#DC2626]" },
  { id: "critic_node", label: "Critic", icon: AlertTriangle, color: "text-[#D97706]", bg: "bg-[#D97706]/10", border: "border-[#D97706]" },
  { id: "final_response", label: "Done", icon: CheckCircle2, color: "text-[#22C55E]", bg: "bg-[#22C55E]/10", border: "border-[#22C55E]" },
];

export default function ChatArea({
  token,
  username,
  currentConvId,
  setCurrentConvId,
  messages,
  setMessages,
  setConversations,
  onAuthExpired,
  onOpenSloModal,
}) {
  const [prompt, setPrompt] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [activePhase, setActivePhase] = useState("");
  const [streamingStatus, setStreamingStatus] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingStatus]);

  const handleSend = async (e) => {
    e.preventDefault();
    const query = prompt.trim();
    if (!query || streaming) return;

    let convId = currentConvId;
    if (!convId) {
      const newConv = await createConversation(token, username);
      convId = newConv.id;
      setCurrentConvId(convId);
    }

    // Append user message
    const currentTime = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const userMsg = { role: "user", content: query, time: currentTime };
    setMessages((prev) => [...prev, userMsg]);
    setPrompt("");
    setStreaming(true);
    setActivePhase("query");
    setStreamingStatus("Thinking...");

    try {
      const { answer, note, route, confidence, status } = await sendQueryStream(
        query,
        convId,
        token,
        username,
        (label, phase) => {
          setStreamingStatus(label);
          if (phase) setActivePhase(phase);
        }
      );

      const assistantMsg = {
        role: "assistant",
        content: answer,
        note,
        route,
        confidence,
        status,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setActivePhase("final_response");

      // Refresh conversations list to update title
      const res = await listConversations(token, username);
      if (res.conversations) {
        setConversations(res.conversations);
      }
    } catch (err) {
      if (err.message === "EXPIRED_SESSION") {
        onAuthExpired();
        return;
      }
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Something went wrong: ${err.message}`,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setStreaming(false);
      setStreamingStatus("");
    }
  };

  return (
    <main className="flex-1 flex flex-col h-screen bg-[#F8FAFC] text-slate-800 overflow-hidden relative">
      {/* Header (Matching Modern Finance Mockup with Top Stream Pipeline) */}
      <header className="px-6 py-3.5 border-b border-slate-200/80 bg-white/90 backdrop-blur-md flex items-center justify-between z-10 shadow-sm gap-4">
        <div className="flex items-center gap-3 shrink-0">
          <Logo className="w-6 h-7 shrink-0" />
          <h1 className="text-base font-bold text-slate-900 tracking-tight hidden lg:block">
            Finance Risk &amp; Investment Intelligence
          </h1>
        </div>

        {/* Multi-Agent Stream Pipeline beside Title */}
        <div className="flex items-center gap-2 overflow-x-auto py-1 px-3 bg-slate-50 border border-slate-200/80 rounded-full shadow-inner">
          {AGENT_NODES.map((node, i) => {
            const Icon = node.icon;
            const isActive = activePhase === node.id || (streaming && activePhase === "");
            return (
              <React.Fragment key={node.id}>
                {i > 0 && <div className="w-3 h-0.5 bg-slate-200 shrink-0" />}
                <div className="flex items-center gap-1.5 shrink-0" title={node.label}>
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center transition-all ${node.bg
                      } ${node.color} ${isActive ? `ring-2 ${node.border} scale-110` : "opacity-75"}`}
                  >
                    <Icon className="w-3 h-3" />
                  </div>
                  <span className={`text-[11px] font-semibold hidden md:inline ${node.color}`}>
                    {node.label}
                  </span>
                </div>
              </React.Fragment>
            );
          })}
        </div>

        <button
          type="button"
          onClick={onOpenSloModal}
          title="Open SLO & System Performance Metrics Dashboard"
          className="flex items-center gap-1.5 py-1.5 px-3.5 rounded-full bg-blue-50 hover:bg-blue-100 text-[#2563EB] border border-blue-200/80 font-semibold text-xs transition shadow-sm shrink-0 active:scale-95 cursor-pointer z-10"
        >
          <Gauge className="w-4 h-4 text-[#2563EB]" />
          <span className="hidden sm:inline">SLO Metrics</span>
        </button>
      </header>

      {/* Messages Stream Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
        {messages.length === 0 ? (
          <div className="max-w-xl mx-auto my-16 p-8 rounded-2xl bg-white border border-slate-200/90 text-center space-y-4 shadow-xl">
            <div className="inline-flex p-3 rounded-2xl bg-blue-50 text-[#2563EB]">
              <Bot className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-900">Finance Risk Intelligence</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Hi — ask me something like{" "}
              <span className="italic text-slate-800 font-medium">
                &quot;What are the key risks in the current investment portfolio?&quot;
              </span>{" "}
              or{" "}
              <span className="italic text-slate-800 font-medium">
                &quot;Which holdings are underperforming their benchmark?&quot;
              </span>
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => {
            const isUser = msg.role === "user";
            return (
              <div
                key={idx}
                className={`flex gap-3.5 max-w-3xl ${isUser ? "ml-auto flex-row-reverse" : "mr-auto"
                  }`}
              >
                <div
                  className={`w-9 h-9 rounded-2xl flex items-center justify-center shrink-0 shadow-sm ${isUser
                    ? "bg-[#2563EB] text-white"
                    : "bg-blue-50 border border-blue-100 text-[#2563EB]"
                    }`}
                >
                  {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                </div>

                <div className="space-y-1">
                  <div
                    className={`rounded-2xl p-4 text-sm leading-relaxed shadow-sm ${isUser
                      ? "bg-[#2563EB] text-white"
                      : "bg-white border border-slate-200 text-slate-800"
                      }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  </div>
                  <div
                    className={`text-[10px] text-slate-400 px-1 ${isUser ? "text-right" : "text-left"
                      }`}
                  >
                    {msg.time || "10:30 AM"}
                  </div>
                </div>
              </div>
            );
          })
        )}

        {/* Live SSE Streaming Status Card */}
        {streaming && (
          <div className="flex gap-3 max-w-3xl mr-auto animate-fade-in">
            <div className="w-9 h-9 rounded-2xl bg-blue-50 border border-blue-100 text-[#2563EB] flex items-center justify-center shrink-0 shadow-sm">
              <Bot className="w-5 h-5 animate-pulse" />
            </div>

            <div className="rounded-2xl p-4 bg-white border border-blue-200 text-slate-800 shadow-md space-y-2 flex-1">
              <div className="flex items-center gap-2.5 text-xs text-[#2563EB] font-semibold">
                <Loader2 className="w-4 h-4 animate-spin text-[#2563EB]" />
                <span>{streamingStatus || "Multi-Agent Workflow analyzing..."}</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>



      {/* Input Box & Send Button */}
      <footer className="p-4 border-t border-slate-200/80 bg-white z-10">
        <form onSubmit={handleSend} className="max-w-4xl mx-auto flex items-center gap-2 relative">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={streaming}
            placeholder="Type your message here..."
            className="w-full bg-white border border-slate-200 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-2xl py-3.5 pl-4 pr-14 text-slate-800 placeholder-slate-400 text-sm outline-none transition shadow-sm disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={streaming || !prompt.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 w-9 h-9 rounded-full bg-[#2563EB] hover:bg-blue-600 text-white flex items-center justify-center transition shadow-md shadow-blue-600/30 disabled:opacity-40"
          >
            <Send className="w-4 h-4 ml-0.5" />
          </button>
        </form>
      </footer>
    </main>
  );
}
