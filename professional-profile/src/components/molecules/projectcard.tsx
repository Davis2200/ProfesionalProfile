"use client";

import { motion } from "framer-motion";
import { IProject } from "@/models/proyectos";
import Link from "next/link";

// Aplanamos la interfaz extrayendo solo las llaves necesarias del modelo global
interface ProjectCardProps extends Readonly<Pick<IProject, "id" | "title" | "metric" | "description" | "tag" | "link">> {}

// Destructuramos las propiedades directas en la firma del componente
export const ProjectCard = ({ id, title, metric, description, tag, link }: ProjectCardProps) => (
  <motion.div 
    whileHover={{ y: -5 }}
    className="group bg-brand-surface border border-slate-200 p-10 rounded-technical 
               shadow-(--shadow-soft) hover:border-brand-action/30 transition-all"
  >
    <div className="flex justify-between items-start">
      <span className="text-[10px] font-black uppercase tracking-widest text-brand-ethics 
                       bg-brand-ethics/10 px-2 py-1 rounded">
        {tag}
      </span>
      <div className="text-right font-mono text-brand-action">
        <p className="text-[10px] uppercase font-bold text-slate-400">Impacto Científico</p>
        <p className="text-xl font-black tracking-tighter">{metric}</p>
      </div>
    </div>
    
    <h3 className="text-2xl font-bold mt-8 text-brand-text group-hover:text-brand-action transition-colors">
      {title}
    </h3>
    <p className="text-slate-500 text-sm mt-4 leading-relaxed font-medium">
      {description}
    </p>
    <div className="mt-8 pt-6 border-t border-slate-200 flex flex-wrap justify-between items-center gap-4">
  <Link 
    href={`/proyectos/${id}`} 
    className="text-[10px] font-black uppercase tracking-tighter text-brand-text hover:text-brand-action transition-colors inline-flex items-center gap-1"
  >
    Metodología <span className="text-sm">→</span>
  </Link>
  
  <a 
    href={link} 
    target="_blank" 
    rel="noopener noreferrer"
    className="text-[10px] font-black uppercase tracking-tighter text-brand-action border border-brand-action/20 px-3 py-1 rounded-full hover:bg-brand-action hover:text-white transition-all inline-flex items-center gap-1"
  >
    Ejecutar Predictor <span className="text-sm">↗</span>
  </a>
</div>
 
  </motion.div>
);