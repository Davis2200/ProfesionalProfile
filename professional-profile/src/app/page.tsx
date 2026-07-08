"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  // Acto I: Rotación dinámica de fortalezas
  const roles = [
    "Modelado Predictivo",
    "Gobernanza de Datos",
    "Desarrollo Full Stack",
  ];
  const [currentRole, setCurrentRole] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentRole((prev) => (prev + 1) % roles.length);
    }, 3500);
    return () => clearInterval(timer);
  }, [roles.length]);

  return (
    <div className="flex flex-col min-h-screen">
      {/* ACTO I: La Génesis */}
      <section id="genesis" className="relative h-screen flex flex-col items-center justify-center bg-aurora-tranquil px-6">
        <div className="z-10 flex flex-col items-center gap-8">
          {/* SVG Construcción (Doherty Threshold < 400ms visual feedback) */}
          <svg width="100" height="100" viewBox="0 0 100 100" className="overflow-visible">
            <motion.path
              d="M10,90 L50,10 L90,90 Z" /* Reemplazar con el path de tu logo real */
              fill="transparent"
              stroke="var(--color-foreground)"
              strokeWidth="3"
              className="logo-path-draw"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 2.2, ease: [0.65, 0, 0.35, 1] }}
            />
          </svg>

          <div className="text-center h-24">
            <AnimatePresence mode="wait">
              <motion.h1
                key={roles[currentRole]}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.4 }}
                className="font-display text-5xl md:text-7xl"
              >
                {roles[currentRole]}
              </motion.h1>
            </AnimatePresence>
          </div>
        </div>
      </section>

      {/* ACTO II: La Tríada del Conocimiento (Bento Box Grid) */}
      <section id="skills" className="py-32 container mx-auto px-6">
        <h2 className="font-display text-4xl mb-16">Arquitectura & Algoritmos</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {["DBSCAN & K-Means", "Next.js 15+ & React", "HDFS & Big Data"].map((skill, index) => (
            <motion.div
              key={skill}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ delay: index * 0.05, duration: 0.4 }} // Miller's Law: Stagger Effect 50ms
              className="glass-card flex flex-col justify-between min-h-[200px]"
            >
              <div className="text-[var(--color-rosa-vibrante)] text-3xl mb-4">✦</div>
              <h3 className="font-bold text-xl">{skill}</h3>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ACTO III: La Evidencia Técnica */}
      <section id="projects" className="py-32 bg-white/5">
        <div className="container mx-auto px-6">
          <h2 className="font-display text-4xl mb-16">Deep Dives</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
            {/* Proyecto 1: E-commerce Demo */}
            <div className="glass-card group cursor-pointer relative overflow-hidden">
              <div className="relative z-10 flex flex-col gap-6">
                <div>
                  <h3 className="font-display text-3xl mb-2">Ecosistema E-commerce</h3>
                  <p className="text-sm opacity-80 max-w-md">Integración bidireccional entre FastApi y Next.js. Procesamiento de pagos vía Stripe Webhooks con latencia optimizada.</p>
                </div>
                {/* Fitts's Law: Área táctil expandida */}
                <button className="btn-action self-start mt-4">
                  Analizar Estructura
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ACTO IV: Vínculo Humano y CTA */}
      <section id="contact" className="py-32 container mx-auto px-6 max-w-3xl">
        <div className="flex flex-col gap-12 items-center">
          
          {/* Continuidad Espacial: Reproductor integrado minimalista */}
          <div className="flex items-center gap-4 bg-[var(--color-glass-surface)] border border-[var(--color-glass-border)] rounded-full px-6 py-3 shadow-sm">
            <span className="text-xl">🏀</span>
            <div className="w-px h-4 bg-gray-300"></div>
            <div className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-[var(--color-rosa-vibrante)] animate-pulse"></div>
              <span className="text-xs font-bold tracking-widest uppercase">Now Playing: Focusrite Sessions</span>
            </div>
            <div className="w-px h-4 bg-gray-300"></div>
            <span className="text-xl">🎵</span>
          </div>

          {/* Peak-End Rule: Formulario Liberal / Validación Conservadora */}
          <form className="glass-card w-full flex flex-col gap-6" onSubmit={(e) => e.preventDefault()}>
            <div className="mb-4 space-y-2">
              <h2 className="font-display text-3xl">Iniciemos el sistema.</h2>
              {/* Gobernanza por Diseño: Badge de Integridad */}
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-green-50 text-green-700 text-xs font-bold rounded-md border border-green-200">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/></svg>
                Transmisión encriptada end-to-end.
              </div>
            </div>
            
            <input 
              type="text" 
              placeholder="¿Cuál es el vector de ataque/proyecto?" 
              className="w-full bg-transparent border-b-2 border-[var(--color-glass-border)] py-4 outline-none focus:border-[var(--color-rosa-vibrante)] transition-colors"
            />
            <button className="btn-action w-full mt-4 group">
              Ejecutar Secuencia
              <span className="group-active:scale-95 transition-transform duration-150 block">↗</span>
            </button>
          </form>

          {/* Hick's Law: 3 Opciones Máximas */}
          <div className="flex gap-8 mt-8 text-sm font-bold uppercase tracking-widest text-[var(--color-violeta-seguridad)]">
            <a href="#" className="hover:text-[var(--color-rosa-vibrante)] transition-colors">LinkedIn</a>
            <a href="#" className="hover:text-[var(--color-rosa-vibrante)] transition-colors">GitHub</a>
            <a href="#" className="hover:text-[var(--color-rosa-vibrante)] transition-colors">WhatsApp</a>
          </div>
        </div>
      </section>
    </div>
  );
}