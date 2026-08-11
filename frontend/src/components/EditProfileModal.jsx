import React, { useState } from "react";
import { X, User, Lock, CheckCircle2, AlertCircle, Loader2, KeyRound } from "lucide-react";
import { updateProfile } from "../api";

export default function EditProfileModal({
  isOpen,
  onClose,
  token,
  username,
  onProfileUpdated,
}) {
  const [name, setName] = useState(username || "");
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (newPassword && !oldPassword) {
      setError("Please enter your Old Password to set a New Password.");
      return;
    }

    if (newPassword && newPassword.length < 6) {
      setError("New Password must be at least 6 characters long.");
      return;
    }

    setLoading(true);

    try {
      const res = await updateProfile(name, oldPassword, newPassword, token, username);
      setSuccess(res.message || "Profile updated successfully!");
      if (res.name) {
        onProfileUpdated(res.name);
      }
      setOldPassword("");
      setNewPassword("");
      setTimeout(() => {
        setSuccess("");
        onClose();
      }, 1500);
    } catch (err) {
      setError(err.message || "Failed to update profile.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4 select-none animate-fade-in">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden relative text-slate-200">
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/50">
          <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
            <User className="w-4 h-4 text-[#2563EB]" />
            Edit Profile Details
          </h3>
          <button
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-lg transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          {error && (
            <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 flex items-start gap-2.5 text-red-400 text-xs">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {success && (
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center gap-2.5 text-emerald-400 text-xs">
              <CheckCircle2 className="w-4 h-4 shrink-0" />
              <span>{success}</span>
            </div>
          )}

          {/* Full Name */}
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Full Name / Username
            </label>
            <div className="relative">
              <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your Full Name"
                className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
              />
            </div>
          </div>

          <div className="h-px bg-slate-800/80 my-2" />

          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block">
            Change Password (Optional)
          </span>

          {/* Old Password */}
          <div>
            <label className="block text-[11px] text-slate-400 mb-1">Old Password</label>
            <div className="relative">
              <KeyRound className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="password"
                value={oldPassword}
                onChange={(e) => setOldPassword(e.target.value)}
                placeholder="Enter current password to change"
                className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
              />
            </div>
          </div>

          {/* New Password */}
          <div>
            <label className="block text-[11px] text-slate-400 mb-1">New Password</label>
            <div className="relative">
              <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="New password (min 6 chars)"
                className="w-full bg-slate-950/70 border border-slate-800 focus:border-[#2563EB] focus:ring-1 focus:ring-[#2563EB] rounded-xl py-2.5 pl-10 pr-4 text-slate-100 placeholder-slate-600 text-xs outline-none transition"
              />
            </div>
          </div>

          {/* Submit */}
          <div className="pt-2 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="bg-[#2563EB] hover:bg-blue-600 text-white font-medium px-4 py-2 rounded-xl text-xs flex items-center gap-2 transition disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Saving...
                </>
              ) : (
                "Save Changes"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
