import React from "react";

export function Logo({ className = "w-8 h-8" }) {
  return (
    <svg viewBox="0 0 120 140" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
      <defs>
        <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#1E40AF" />
          <stop offset="50%" stopColor="#1D4ED8" />
          <stop offset="100%" stopColor="#0F172A" />
        </linearGradient>
        <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#FDE047" />
          <stop offset="50%" stopColor="#EAB308" />
          <stop offset="100%" stopColor="#CA8A04" />
        </linearGradient>
        <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#FFFFFF" />
          <stop offset="100%" stopColor="#CBD5E1" />
        </linearGradient>
      </defs>
      {/* Outer Gold Shield Border */}
      <path
        d="M60 4 L112 24 V68 C112 100 88 126 60 136 C32 126 8 100 8 68 V24 L60 4 Z"
        fill="url(#goldGrad)"
      />
      {/* Inner Blue Shield */}
      <path
        d="M60 10 L106 28 V66 C106 94 84 118 60 128 C36 118 14 94 14 66 V28 L60 10 Z"
        fill="url(#shieldGrad)"
        stroke="#FACC15"
        strokeWidth="1.5"
      />
      {/* Dollar Sign */}
      <text x="24" y="86" fill="#FDE047" fontSize="22" fontWeight="bold" fontFamily="sans-serif">$</text>
      {/* Bar Chart Bars */}
      <rect x="52" y="70" width="10" height="28" rx="2" fill="url(#barGrad)" />
      <rect x="67" y="56" width="10" height="42" rx="2" fill="url(#barGrad)" />
      <rect x="82" y="42" width="10" height="56" rx="2" fill="url(#barGrad)" />
      {/* Ascending Trend Line */}
      <path
        d="M20 72 L45 52 L68 58 L96 32"
        stroke="url(#goldGrad)"
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Arrowhead */}
      <path d="M86 30 L98 30 L96 42 Z" fill="#FDE047" />
      {/* Node Dots */}
      <circle cx="45" cy="52" r="4" fill="#FDE047" />
      <circle cx="68" cy="58" r="4" fill="#FDE047" />
    </svg>
  );
}
