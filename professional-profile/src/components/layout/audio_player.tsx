"use client";
import { useState } from 'react';

export default function AudioPlayer() {
  return (
    <div className="fixed bottom-8 left-8 z-50 flex items-center gap-4 glass-card py-3 px-6 rounded-full shadow-lg">
      <div className="flex items-center gap-3">
        <span className="text-xl animate-pulse">🎵</span>
        <div className="flex flex-col">
          <span className="text-[10px] uppercase font-black tracking-tighter opacity-60">Now Playing</span>
          <span className="text-xs font-bold font-display">Focusrite Sessions</span>
        </div>
      </div>
      
      {/* Fitts's Law: Área táctil > 44px */}
      <button className="w-10 h-10 flex items-center justify-center rounded-full bg-[var(--color-rosa-vibrante)] text-white active:scale-95 transition-transform">
        <span>🏀</span>
      </button>
    </div>
  );
}