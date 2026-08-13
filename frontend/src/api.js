function getApiBaseUrl() {
  if (typeof window !== "undefined") {
    const hostname = window.location.hostname;
    // When running locally on localhost, ALWAYS use the local backend server
    if (hostname === "localhost" || hostname === "127.0.0.1" || hostname === "0.0.0.0") {
      return "http://localhost:8000";
    }
  }
  // When deployed live, use VITE_API_BASE_URL if set, or relative URL "" for vercel/host rewrites
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  return "";
}

const API_BASE_URL = getApiBaseUrl();

function getAuthHeaders(token, username, extra = {}) {
  const headers = { ...extra };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  if (username) {
    headers["X-User"] = username;
  }
  return headers;
}

export async function register(name, email, password) {
  const cleanName = name.trim();
  const cleanEmail = email.trim().toLowerCase();
  if (!cleanName) {
    throw new Error("Please enter your name.");
  }
  if (!cleanEmail || !cleanEmail.includes("@")) {
    throw new Error("Please enter a valid email address.");
  }
  if (!password || password.length < 6) {
    throw new Error("Password must be at least 6 characters long.");
  }

  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: cleanName, email: cleanEmail, password }),
  });

  if (!res.ok) {
    let errMsg = `Registration failed (${res.status})`;
    try {
      const data = await res.json();
      if (data.detail) errMsg = data.detail;
    } catch (_) { }
    throw new Error(errMsg);
  }

  return await res.json(); // { message, email, requires_verification }
}

export async function login(username, password) {
  const cleanUsername = username.trim().toLowerCase();
  if (!cleanUsername || !password || !cleanUsername.includes("@")) {
    throw new Error("Please enter a valid email address and password.");
  }

  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: cleanUsername, password }),
  });

  if (!res.ok) {
    let errMsg = `Authentication failed (${res.status})`;
    try {
      const data = await res.json();
      if (data.detail) errMsg = data.detail;
    } catch (_) { }
    throw new Error(errMsg);
  }

  return await res.json(); // { access_token, username, email }
}

export async function updateProfile(name, oldPassword, newPassword, token, username) {
  const payload = {};
  if (name && name.trim()) payload.name = name.trim();
  if (oldPassword) payload.old_password = oldPassword;
  if (newPassword) payload.new_password = newPassword;

  const res = await fetch(`${API_BASE_URL}/auth/profile/update`, {
    method: "POST",
    headers: getAuthHeaders(token, username, { "Content-Type": "application/json" }),
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Failed to update profile");
  }
  return data; // { message, name }
}

export async function getSLOMetrics(token, username) {
  try {
    const res = await fetch(`${API_BASE_URL}/slo/metrics`, {
      headers: getAuthHeaders(token, username),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error("Failed to fetch SLO metrics:", err);
    return null;
  }
}

export async function resetSLOMetrics(token, username) {
  try {
    const res = await fetch(`${API_BASE_URL}/slo/reset`, {
      method: "POST",
      headers: getAuthHeaders(token, username),
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (err) {
    console.error("Failed to reset SLO metrics:", err);
    return null;
  }
}

export async function listConversations(token, username) {
  try {
    const res = await fetch(`${API_BASE_URL}/conversations`, {
      headers: getAuthHeaders(token, username),
    });
    if (res.status === 401 || res.status === 403) return { expired: true, conversations: [] };
    if (!res.ok) return { conversations: [] };
    const data = await res.json();
    return { conversations: data.conversations || [] };
  } catch (err) {
    console.error("Failed to list conversations:", err);
    return { conversations: [] };
  }
}

export async function createConversation(token, username) {
  try {
    const res = await fetch(`${API_BASE_URL}/conversations`, {
      method: "POST",
      headers: getAuthHeaders(token, username),
    });
    if (!res.ok) return { id: "local_" + Date.now(), title: "New conversation" };
    return await res.json();
  } catch (err) {
    return { id: "local_" + Date.now(), title: "New conversation" };
  }
}

export async function getMessages(conversationId, token, username) {
  if (!conversationId) return [];
  try {
    const res = await fetch(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
      headers: getAuthHeaders(token, username),
    });
    if (!res.ok) return [];
    const data = await res.json();
    return data.messages || [];
  } catch (err) {
    console.error("Failed to fetch messages:", err);
    return [];
  }
}

export async function deleteConversation(conversationId, token, username) {
  try {
    const res = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
      method: "DELETE",
      headers: getAuthHeaders(token, username),
    });
    return res.ok;
  } catch (err) {
    console.error("Failed to delete conversation:", err);
    return false;
  }
}

export async function listDocuments(token, username) {
  try {
    const res = await fetch(`${API_BASE_URL}/rag/documents`, {
      headers: getAuthHeaders(token, username),
    });
    if (!res.ok) return [];
    const data = await res.json();
    return data.documents || [];
  } catch (err) {
    return [];
  }
}

export async function uploadDocument(file, token, username) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/rag/ingest`, {
    method: "POST",
    headers: getAuthHeaders(token, username),
    body: formData,
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Upload failed");
  }
  return data;
}

export async function removeDocument(filename, token, username) {
  const res = await fetch(`${API_BASE_URL}/rag/documents/${encodeURIComponent(filename)}`, {
    method: "DELETE",
    headers: getAuthHeaders(token, username),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Remove failed");
  }
  return data.documents || [];
}

export async function getSqlSchema(token, username) {
  try {
    const res = await fetch(`${API_BASE_URL}/sql/schema`, {
      headers: getAuthHeaders(token, username),
    });
    if (!res.ok) return [];
    const data = await res.json();
    return data.tables || [];
  } catch (err) {
    return [];
  }
}

export async function uploadSql(file, token, username) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE_URL}/sql/ingest`, {
      method: "POST",
      headers: getAuthHeaders(token, username),
      body: formData,
    });

    const contentType = res.headers.get("content-type") || "";
    let data;
    if (contentType.includes("application/json")) {
      data = await res.json();
    } else {
      const text = await res.text();
      data = { detail: text || `Server error (${res.status})` };
    }

    if (!res.ok) {
      throw new Error(data.detail || `SQL ingestion failed (${res.status})`);
    }
    return data;
  } catch (err) {
    if (err.name === "TypeError" && err.message === "Failed to fetch") {
      throw new Error("Could not connect to backend server or upload was blocked by CORS/network.");
    }
    throw err;
  }
}

export const PHASE_LABELS = {
  crew_node: "Thinking...",
  critic_node: "Reviewing answer...",
  route_decision: "Finalizing response...",
  final_response: "Response ready",
};

export async function sendQueryStream(query, conversationId, token, username, onPhaseChange) {
  try {
    const response = await fetch(`${API_BASE_URL}/query/stream`, {
      method: "POST",
      headers: getAuthHeaders(token, username, { "Content-Type": "application/json" }),
      body: JSON.stringify({ query, conversation_id: conversationId }),
    });

    if (response.status === 401 || response.status === 403) {
      throw new Error("EXPIRED_SESSION");
    }

    if (!response.ok) {
      throw new Error(`Stream request failed (${response.status})`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let bestPayload = null;

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed.startsWith("data: ")) continue;

        const dataStr = trimmed.slice(6);
        try {
          const data = JSON.parse(dataStr);
          if (data.phase === "error") {
            throw new Error(data.message || "Workflow error");
          }

          let label = PHASE_LABELS[data.phase] || data.phase;
          if (data.revise_count && data.revise_count > 0) {
            label += ` (revision ${data.revise_count})`;
          }
          if (onPhaseChange) onPhaseChange(label);

          if (data.final_response) {
            bestPayload = data;
          }
        } catch (e) {
          if (e.message === "EXPIRED_SESSION" || e.message.includes("Workflow error")) throw e;
          // ignore parse errors for chunks
        }
      }
    }

    if (!bestPayload) {
      throw new Error("Stream ended without a final response");
    }

    return {
      answer: bestPayload.final_response,
      note: null,
      route: bestPayload.route,
      confidence: bestPayload.confidence,
      status: bestPayload.status,
    };
  } catch (err) {
    if (err.message === "EXPIRED_SESSION") throw err;

    // Fallback to plain non-streaming endpoint
    if (onPhaseChange) onPhaseChange("Falling back to standard request...");

    const fallbackRes = await fetch(`${API_BASE_URL}/query`, {
      method: "POST",
      headers: getAuthHeaders(token, username, { "Content-Type": "application/json" }),
      body: JSON.stringify({ query, conversation_id: conversationId }),
    });

    if (fallbackRes.status === 401 || fallbackRes.status === 403) {
      throw new Error("EXPIRED_SESSION");
    }

    if (!fallbackRes.ok) {
      let errDetail = `Request failed (${fallbackRes.status})`;
      try {
        const body = await fallbackRes.json();
        if (body.detail) errDetail = body.detail;
      } catch (_) { }
      throw new Error(errDetail);
    }

    const data = await fallbackRes.json();

    return {
      answer: data.final_response || "(no response)",
      note: null,
      route: data.route,
      confidence: data.confidence,
      status: data.status,
    };
  }
}
