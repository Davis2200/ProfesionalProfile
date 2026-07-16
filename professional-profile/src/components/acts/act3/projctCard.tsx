"use client";
import { motion } from "framer-motion";

interface ProjectCardProps {
  readonly title: string;
  readonly description: string;
  readonly tags: string[];
  readonly onClick: () => void;
}

export default function ProjectCard({ title, description, tags, onClick }: ProjectCardProps) {
  return (
    <motion.div 
      whileHover={{ scale: 1.02 }}
      className="glass-card cursor-pointer group"
      onClick={onClick}
      role="button"
      aria-label={`Ver detalles de ${title}`}
    >
      <h3 className="text-2xl font-display mb-3 group-hover:text-[var(--color-rosa-vibrante)] transition-colors">
        {title}
      </h3>
      <p className="text-sm opacity-80 mb-6 line-clamp-2">{description}</p>
      
      <div className="flex flex-wrap gap-2 mb-6">
        {tags.map(tag => (
          <span key={tag} className="text-[10px] uppercase tracking-widest border border-[var(--color-glass-border)] px-2 py-1 rounded-md">
            {tag}
          </span>
        ))}
      </div>

      {/* Fitts's Law: Área táctil expandida > 44px */}
      <button className="btn-action w-full py-3 text-xs uppercase tracking-tighter">
        Explorar Deep Dive
      </button>
    </motion.div>
  );
}