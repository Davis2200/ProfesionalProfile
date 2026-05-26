"use client";
import { motion } from "framer-motion";


export const Navbar = () => (
  <nav className="fixed top-0 w-full z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
    <div className="max-w-6xl mx-auto px-6 h-20 flex justify-between items-center text-brand-text">
      <div className="font-black tracking-tighter text-black">
        <a href="/">DAVID<span className="text-brand-action">NAVA.</span></a>
       </div>

      <div className="hidden md:flex gap-10 text-[10px] font-black uppercase tracking-[0.25em] text-slate-400">
        <a href="/#proyectos" className="hover:text-brand-action transition-colors">Proyectos</a>
        <a href="/ciencia" className="hover:text-brand-action transition-colors">Ciencia</a>
        <a href="/about" className="hover:text-brand-ethics transition-colors">Responsabilidad</a>
      </div>

      <button className="text-[10px] font-black uppercase tracking-widest border-2 border-brand-text px-6 py-2 rounded-technical hover:bg-brand-text hover:text-white transition-all">
        Contacto
      </button>
    </div>
  </nav>
);