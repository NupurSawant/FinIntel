import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import SLODashboardModal from "./components/SLODashboardModal";
import {
  listConversations,
  getMessages,
  listDocuments,
  getSqlSchema,
} from "./api";

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("access_token") || "");
  const [username, setUsername] = useState(() => localStorage.getItem("display_name") || "");
  const [userEmail, setUserEmail] = useState(() => localStorage.getItem("user_email") || "");

  const [conversations, setConversations] = useState([]);
  const [currentConvId, setCurrentConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [ragDocuments, setRagDocuments] = useState([]);
  const [sqlTables, setSqlTables] = useState([]);
  const [loadingApp, setLoadingApp] = useState(true);
  const [isSloModalOpen, setIsSloModalOpen] = useState(false);

  const handleLoginSuccess = (newToken, newUsername, newEmail) => {
    localStorage.setItem("access_token", newToken);
    localStorage.setItem("display_name", newUsername);
    if (newEmail) localStorage.setItem("user_email", newEmail);
    setToken(newToken);
    setUsername(newUsername);
    setUserEmail(newEmail || newUsername);
  };

  const handleProfileUpdated = (newName) => {
    localStorage.setItem("display_name", newName);
    setUsername(newName);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("display_name");
    localStorage.removeItem("user_email");
    setToken("");
    setUsername("");
    setUserEmail("");
    setConversations([]);
    setCurrentConvId(null);
    setMessages([]);
    setRagDocuments([]);
    setSqlTables([]);
  };

  // Synchronize state when authenticated
  useEffect(() => {
    if (!token) {
      setLoadingApp(false);
      return;
    }

    let isMounted = true;
    async function loadInitialData() {
      setLoadingApp(true);
      const convRes = await listConversations(token, username);
      if (convRes.expired) {
        handleLogout();
        setLoadingApp(false);
        return;
      }

      if (!isMounted) return;
      const convs = convRes.conversations || [];
      setConversations(convs);

      let activeId = currentConvId;
      if (!activeId && convs.length > 0) {
        activeId = convs[0].id;
        setCurrentConvId(activeId);
      }

      if (activeId) {
        const msgs = await getMessages(activeId, token, username);
        if (isMounted) setMessages(msgs);
      }

      const docs = await listDocuments(token, username);
      if (isMounted) setRagDocuments(docs);

      const tables = await getSqlSchema(token, username);
      if (isMounted) setSqlTables(tables);

      if (isMounted) setLoadingApp(false);
    }

    loadInitialData();

    return () => {
      isMounted = false;
    };
  }, [token, username]);

  // Load messages when currentConvId changes
  useEffect(() => {
    if (!token || !currentConvId) return;
    let isMounted = true;
    getMessages(currentConvId, token, username).then((msgs) => {
      if (isMounted) setMessages(msgs);
    });
    return () => {
      isMounted = false;
    };
  }, [currentConvId]);

  if (!token) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  if (loadingApp) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <span>Loading workspace...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950">
      <Sidebar
        token={token}
        username={username}
        userEmail={userEmail}
        conversations={conversations}
        setConversations={setConversations}
        currentConvId={currentConvId}
        setCurrentConvId={setCurrentConvId}
        setMessages={setMessages}
        ragDocuments={ragDocuments}
        setRagDocuments={setRagDocuments}
        sqlTables={sqlTables}
        setSqlTables={setSqlTables}
        onLogout={handleLogout}
        onProfileUpdated={handleProfileUpdated}
      />
      <ChatArea
        token={token}
        username={username}
        currentConvId={currentConvId}
        setCurrentConvId={setCurrentConvId}
        messages={messages}
        setMessages={setMessages}
        setConversations={setConversations}
        onAuthExpired={handleLogout}
        onOpenSloModal={() => setIsSloModalOpen(true)}
      />

      <SLODashboardModal
        isOpen={isSloModalOpen}
        onClose={() => setIsSloModalOpen(false)}
        token={token}
        username={username}
      />
    </div>
  );
}
