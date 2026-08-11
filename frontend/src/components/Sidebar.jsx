import React, { useState } from "react";
import {
  Plus,
  MessageSquare,
  X,
  LogOut,
  FileText,
  Upload,
  Database,
  Paperclip,
  CheckCircle2,
  AlertCircle,
  Loader2,
  ChevronDown,
  Edit3,
} from "lucide-react";
import { Logo } from "./Logo";
import EditProfileModal from "./EditProfileModal";
import {
  createConversation,
  deleteConversation,
  uploadDocument,
  removeDocument,
  uploadSql,
  listDocuments,
} from "../api";

export default function Sidebar({
  token,
  username,
  userEmail,
  conversations,
  setConversations,
  currentConvId,
  setCurrentConvId,
  setMessages,
  ragDocuments,
  setRagDocuments,
  sqlTables,
  setSqlTables,
  onLogout,
  onProfileUpdated,
}) {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedDocFiles, setSelectedDocFiles] = useState([]);
  const [docUploading, setDocUploading] = useState(false);
  const [docFeedback, setDocFeedback] = useState(null);

  const [selectedSqlFile, setSelectedSqlFile] = useState(null);
  const [sqlUploading, setSqlUploading] = useState(false);
  const [sqlFeedback, setSqlFeedback] = useState(null);

  const avatarLetter = username ? username[0].toUpperCase() : "N";

  // ---- New Chat ----
  const handleNewChat = async () => {
    const conv = await createConversation(token, username);
    setConversations((prev) => {
      const exists = prev.some((c) => c.id === conv.id);
      return exists ? prev : [conv, ...prev];
    });
    setCurrentConvId(conv.id);
    setMessages([]);
  };

  // ---- Select Chat ----
  const handleSelectChat = (convId) => {
    setCurrentConvId(convId);
  };

  // ---- Delete Chat ----
  const handleDeleteChat = async (e, convId) => {
    e.stopPropagation();
    await deleteConversation(convId, token, username);
    const updatedConvs = conversations.filter((c) => c.id !== convId);
    setConversations(updatedConvs);
    if (currentConvId === convId) {
      if (updatedConvs.length > 0) {
        setCurrentConvId(updatedConvs[0].id);
      } else {
        setCurrentConvId(null);
        setMessages([]);
      }
    }
  };

  // ---- Document Upload ----
  const handleDocUpload = async () => {
    if (!selectedDocFiles || selectedDocFiles.length === 0) return;
    setDocUploading(true);
    setDocFeedback(null);
    let successCount = 0;
    let lastMsg = "";

    try {
      for (const file of selectedDocFiles) {
        try {
          const res = await uploadDocument(file, token, username);
          successCount++;
          lastMsg = `'${res.filename}' indexed — ${res.chunks_ingested} passage(s) added.`;
        } catch (err) {
          lastMsg = `Upload failed for '${file.name}': ${err.message}`;
        }
      }
      if (successCount > 0) {
        const docs = await listDocuments(token, username);
        setRagDocuments(docs);
        setDocFeedback({ type: "success", text: lastMsg });
        setSelectedDocFiles([]);
      } else {
        setDocFeedback({ type: "error", text: lastMsg });
      }
    } finally {
      setDocUploading(false);
    }
  };

  // ---- Remove Document ----
  const handleRemoveDoc = async (filename) => {
    try {
      const updatedDocs = await removeDocument(filename, token, username);
      setRagDocuments(updatedDocs);
    } catch (err) {
      setDocFeedback({ type: "error", text: err.message });
    }
  };

  // ---- SQL Upload ----
  const handleSqlUpload = async () => {
    if (!selectedSqlFile) return;
    setSqlUploading(true);
    setSqlFeedback(null);

    try {
      const res = await uploadSql(selectedSqlFile, token, username);
      setSqlTables(res.tables || []);
      setSqlFeedback({ type: "success", text: res.message });
      setSelectedSqlFile(null);
    } catch (err) {
      setSqlFeedback({ type: "error", text: err.message });
    } finally {
      setSqlUploading(false);
    }
  };

  return (
    <aside className="w-72 bg-[#0F172A] border-r border-slate-800 flex flex-col h-screen text-slate-300 text-sm overflow-hidden select-none shrink-0 shadow-xl">
      {/* 1. Left Top Corner Logo Header */}
      <div className="p-5 flex items-center gap-3">
        <Logo className="w-8 h-9 shrink-0 drop-shadow-md" />
        <div className="font-bold text-white text-base tracking-tight leading-tight">
          Finance Intelligence
        </div>
      </div>

      {/* 2. New Chat Button */}
      <div className="px-4 mb-4">
        <button
          onClick={handleNewChat}
          className="w-full bg-[#2563EB] hover:bg-blue-600 text-white font-medium py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 transition shadow-lg shadow-blue-600/25 text-sm"
        >
          <Plus className="w-4 h-4" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Scrollable Container */}
      <div className="flex-1 overflow-y-auto px-4 space-y-6">
        {/* Conversations Section */}
        <div>
          <h3 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2 px-2">
            Conversations
          </h3>

          <div className="space-y-1 max-h-44 overflow-y-auto pr-1">
            {conversations.length > 0 ? (
              conversations.map((conv) => {
                const isActive = conv.id === currentConvId;
                return (
                  <div
                    key={conv.id}
                    onClick={() => handleSelectChat(conv.id)}
                    className={`group flex items-center justify-between px-3 py-2.5 rounded-xl cursor-pointer transition text-xs ${
                      isActive
                        ? "bg-[#1E293B] text-white font-semibold border-l-4 border-[#2563EB]"
                        : "hover:bg-[#1E293B]/60 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    <div className="flex items-center gap-2.5 truncate">
                      <MessageSquare
                        className={`w-4 h-4 shrink-0 ${isActive ? "text-[#2563EB]" : "text-slate-500"}`}
                      />
                      <span className="truncate">{conv.title || "New conversation"}</span>
                    </div>
                    <button
                      onClick={(e) => handleDeleteChat(e, conv.id)}
                      title="Delete chat"
                      className="opacity-0 group-hover:opacity-100 p-1 text-slate-500 hover:text-red-400 rounded transition"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  </div>
                );
              })
            ) : (
              <p className="text-xs text-slate-600 italic px-2 py-1">No conversations yet</p>
            )}
          </div>
        </div>

        <div className="h-px bg-slate-800/60" />

        {/* Documents (RAG) Section */}
        <div>
          <h3 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2 px-2">
            Documents
          </h3>

          <div className="space-y-2">
            <input
              type="file"
              id="doc-uploader"
              multiple
              accept=".pdf,.docx,.txt"
              className="hidden"
              onChange={(e) => setSelectedDocFiles(Array.from(e.target.files || []))}
            />
            <label
              htmlFor="doc-uploader"
              className="flex items-center justify-center gap-2 w-full p-2.5 border border-dashed border-slate-700 hover:border-slate-500 rounded-xl cursor-pointer text-xs text-slate-400 hover:text-slate-200 transition bg-slate-950/40"
            >
              <Paperclip className="w-3.5 h-3.5" />
              {selectedDocFiles.length > 0
                ? `${selectedDocFiles.length} file(s) selected`
                : "Attach document(s)"}
            </label>

            {selectedDocFiles.length > 0 && (
              <button
                onClick={handleDocUpload}
                disabled={docUploading}
                className="w-full bg-[#1E293B] hover:bg-slate-700 text-slate-200 font-medium py-2 px-3 rounded-xl flex items-center justify-center gap-2 transition text-xs disabled:opacity-50"
              >
                {docUploading ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload className="w-3.5 h-3.5" />
                    Upload document(s)
                  </>
                )}
              </button>
            )}

            {docFeedback && (
              <div
                className={`p-2 rounded-lg text-xs flex items-center gap-2 ${
                  docFeedback.type === "success"
                    ? "bg-emerald-500/10 border border-emerald-500/20 text-emerald-400"
                    : "bg-red-500/10 border border-red-500/20 text-red-400"
                }`}
              >
                {docFeedback.type === "success" ? (
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                ) : (
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                )}
                <span className="truncate">{docFeedback.text}</span>
              </div>
            )}

            <div className="pt-1">
              {ragDocuments.length > 0 && (
                <div className="space-y-1 max-h-36 overflow-y-auto">
                  {ragDocuments.map((docName) => (
                    <div
                      key={docName}
                      className="flex items-center justify-between p-1.5 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs text-slate-400"
                    >
                      <div className="flex items-center gap-1.5 truncate">
                        <FileText className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                        <span className="truncate">{docName}</span>
                      </div>
                      <button
                        onClick={() => handleRemoveDoc(docName)}
                        title="Remove document"
                        className="p-1 text-slate-500 hover:text-red-400 rounded transition"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="h-px bg-slate-800/60" />

        {/* Database (SQL) Section */}
        <div>
          <h3 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2 px-2">
            SQL Database
          </h3>

          <div className="space-y-2">
            <input
              type="file"
              id="sql-uploader"
              accept=".sql"
              className="hidden"
              onChange={(e) => setSelectedSqlFile(e.target.files ? e.target.files[0] : null)}
            />
            <label
              htmlFor="sql-uploader"
              className="flex items-center justify-center gap-2 w-full p-2.5 border border-dashed border-slate-700 hover:border-slate-500 rounded-xl cursor-pointer text-xs text-slate-400 hover:text-slate-200 transition bg-slate-950/40"
            >
              <Database className="w-3.5 h-3.5" />
              {selectedSqlFile ? selectedSqlFile.name : "Upload a .sql file"}
            </label>

            {selectedSqlFile && (
              <button
                onClick={handleSqlUpload}
                disabled={sqlUploading}
                className="w-full bg-[#1E293B] hover:bg-slate-700 text-slate-200 font-medium py-2 px-3 rounded-xl flex items-center justify-center gap-2 transition text-xs disabled:opacity-50"
              >
                {sqlUploading ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    Ingesting SQL...
                  </>
                ) : (
                  <>
                    <Upload className="w-3.5 h-3.5" />
                    Upload &amp; Ingest
                  </>
                )}
              </button>
            )}

            {sqlFeedback && (
              <div
                className={`p-2 rounded-lg text-xs flex items-center gap-2 ${
                  sqlFeedback.type === "success"
                    ? "bg-emerald-500/10 border border-emerald-500/20 text-emerald-400"
                    : "bg-red-500/10 border border-red-500/20 text-red-400"
                }`}
              >
                {sqlFeedback.type === "success" ? (
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                ) : (
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                )}
                <span className="truncate">{sqlFeedback.text}</span>
              </div>
            )}

            <div className="pt-1">
              {sqlTables && sqlTables.length > 0 && (
                <div className="space-y-1 max-h-36 overflow-y-auto">
                  {sqlTables.map((tbl) => (
                    <div
                      key={tbl}
                      className="flex items-center gap-2 p-1.5 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs text-slate-400"
                    >
                      <Database className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                      <span className="truncate">{tbl}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 3. Bottom User Profile Section (Displaying Name & Email) */}
      <div className="p-4 border-t border-slate-800/80 flex items-center justify-between bg-[#0F172A]">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-8 h-8 rounded-full bg-[#2563EB] font-bold text-white flex items-center justify-center text-xs shadow-md shrink-0">
            {avatarLetter}
          </div>
          <div className="flex flex-col min-w-0 leading-tight">
            <span className="truncate font-semibold text-slate-200 text-xs">
              {username || "Nupur Sawant"}
            </span>
            <span className="truncate text-[11px] text-slate-400">
              {userEmail || (username?.includes("@") ? username : "")}
            </span>
          </div>
        </div>
        <div className="flex items-center gap-1 shrink-0">
          <button
            onClick={() => setIsEditModalOpen(true)}
            title="Edit profile details"
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition"
          >
            <Edit3 className="w-4 h-4" />
          </button>
          <button
            onClick={onLogout}
            title="Log out"
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>

      <EditProfileModal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        token={token}
        username={username}
        onProfileUpdated={onProfileUpdated}
      />
    </aside>
  );
}
