"use client";
import { motion } from "framer-motion";

export default function PersonalSelection() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 my-16">
      <motion.div whileHover={{ scale: 1.02 }} className="glass-card flex items-center gap-6">
        <span className="text-4xl">🏀</span>
        <div>
          <h4 className="text-xl font-display">Estrategia en la Cancha</h4>
          <p className="text-sm opacity-70">El básquetbol me enseñó que los datos, como las jugadas, solo valen si se ejecutan en equipo.</p>
        </div>
      </motion.div>
      <motion.div whileHover={{ scale: 1.02 }} className="glass-card flex items-center gap-6">
        <span className="text-4xl">🎧</span>
        <div>
          <h4 className="text-xl font-display">Frecuencias Técnicas</h4>
          <p className="text-sm opacity-70">Amante del lo-fi y las sesiones de Focusrite; el ritmo perfecto para el modelado de datos.</p>
        </div>
      </motion.div>
    </div>
  );
}