"use client";
import { motion } from "framer-motion";
import * as Icons from "lucide-react"; 

interface SkillItem {
  id: number;
  name: string;
  proficiency_level: number;
}

interface SkillCardProps {
  readonly title: string;
  readonly items: SkillItem[]; // <-- Cambiado a arreglo de objetos
  readonly type: "data" | "fullstack" | "governance";
  readonly iconName: string; 
  readonly index: number;
}

export default function SkillCard({ title, items, type, iconName, index }: SkillCardProps) {
  const Icon = (Icons as any)[iconName] || Icons.Code;
  const accentColor = type === "data" ? "var(--color-rosa-vibrante)" : 
                     type === "governance" ? "var(--color-violeta-seguridad)" : "var(--color-foreground)";

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }} // Stagger Effect 50ms [3, 7]
      className="glass-card flex flex-col h-full group"
    >
      <div className="flex items-center gap-3 mb-4">
        <Icon size={24} style={{ color: accentColor }} />
        <h3 className="text-xl font-display uppercase tracking-tight">{title}</h3>
      </div>
      <ul className="space-y-3">
        {items.map((item, i) => (
          // Usamos item.id como key única o el índice si no viene listo
          <li key={item.id || i} className="text-sm font-sans opacity-70 group-hover:opacity-100 transition-opacity flex items-center gap-2">
            <span className="w-1 h-1 rounded-full" style={{ backgroundColor: accentColor }} />
            {/* SOLUCIÓN: Accedemos de forma segura a item.name en lugar del objeto completo */}
            {item.name} 
          </li>
        ))}
      </ul>
    </motion.div>
  );
}