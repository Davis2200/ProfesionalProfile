"use client";
import { motion } from "framer-motion";

export const Hero = ({ title, subtitle, description }: any) => (
  <section className="relative min-h-[80vh] flex flex-col justify-center items-start max-w-6xl mx-auto px-6 overflow-hidden">
    {/* Efecto de luz suave para evocar innovación */}
    <div className="absolute top-0 right-0 w-125 h-125 bg-brand-action/5 blur-[120px] rounded-full -z-10" />
    
    <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
      <h1 className="text-5xl md:text-7xl font-black tracking-tighter leading-none text-brand-text">
        {title.split(' ').map((word: string, i: number) => (
          <span key={i} className={i >= 2 ? "text-brand-action" : ""}>{word} </span>
        ))}
      </h1>
      <p className="text-brand-ethics font-mono text-sm mt-6 uppercase tracking-[0.3em] font-black">
        {subtitle}
      </p>
      <p className="max-w-2xl mt-8 text-xl text-slate-500 leading-relaxed font-medium">
        {description}
      </p>
      
      <div className="mt-12 flex flex-wrap gap-4">
        <button className="btn-technical">
          Explorar Evidencia Técnica
        </button>
        <button className="px-8 py-4 border border-slate-200 rounded-technical hover:bg-slate-50 
                           transition-all text-sm font-bold text-slate-600">
          Manifiesto Ético
        </button>
      </div>
    </motion.div>
  </section>
);