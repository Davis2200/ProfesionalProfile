"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

const roles = ["Modelado Predictivo", "Gobernanza de Datos", "Desarrollo Full Stack"];

export default function Hero() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setIndex((prev) => (prev + 1) % roles.length), 3500);
    return () => clearInterval(timer);
  }, []);

  return (
    <section className="relative min-h-[80vh] flex items-center justify-center overflow-hidden bg-aurora-tranquil px-4">
      <div className="text-center z-10 max-w-4xl">
        <h1 className="text-5xl md:text-7xl font-black mb-6">
          Arquitectura de <br />
          <AnimatePresence mode="wait">
            <motion.span
              key={roles[index]}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="text-[var(--color-rosa-vibrante)] inline-block"
            >
              {roles[index]}
            </motion.span>
          </AnimatePresence>
        </h1>
        <p className="text-xl opacity-80 mb-10 font-sans max-w-2xl mx-auto">
          Especialista en convertir la complejidad del Big Data en experiencias visuales ligeras y seguras.
        </p>
        <button className="btn-action mx-auto">
          Explorar Evidencia Técnica
        </button>
      </div>
    </section>
  );
}