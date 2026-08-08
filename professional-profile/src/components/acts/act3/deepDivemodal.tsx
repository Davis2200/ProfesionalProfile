"use client";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

// Debe coincidir con el schema ProjectDeepDiveOut del backend (FastAPI)
interface ProjectDeepDive {
  title: string;
  short_description: string;
  thumbnail_url?: string | null;
  tags: string[];
  long_description: string;
  architecture?: string | null;
  results?: string | null;
}

interface DeepDiveModalProps {
  readonly isOpen: boolean;
  readonly onClose: () => void;
  readonly slug: string | null;
}

export default function DeepDiveModal({ isOpen, onClose, slug }: DeepDiveModalProps) {
  const [project, setProject] = useState<ProjectDeepDive | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Efecto para bloquear el scroll de la página principal cuando el modal está abierto
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen || !slug) {
      setProject(null);
      setError(null);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/projects/${slug}`)
      .then((res) => {
        if (!res.ok) throw new Error("No se pudo cargar el detalle del proyecto");
        return res.json();
      })
      .then((data) => {
        if (!cancelled) setProject(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [isOpen, slug]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="glass-card max-w-2xl w-full max-h-[85vh] overflow-y-auto bg-[var(--color-fondo-tranquilo)] border-[var(--color-rosa-vibrante)]"
          >
            {/* Cabecera fija para que el título y botón de cierre no se oculten al hacer scroll */}
            <div className="flex justify-between items-start mb-8 sticky top-0 bg-[var(--color-fondo-tranquilo)]/90 backdrop-blur pb-2 z-10">
              <h2 className="text-3xl font-display">{project?.title ?? "Cargando..."}</h2>
              <button onClick={onClose} className="p-2 hover:bg-black/5 rounded-full transition-colors">✕</button>
            </div>

            {loading && <p className="opacity-70 font-sans">Cargando detalles del proyecto...</p>}
            {error && <p className="text-red-500 font-sans">{error}</p>}

            {!loading && !error && project && (
              <div className="space-y-6 font-sans">
                <div>
                  <h4 className="font-black text-[var(--color-rosa-vibrante)] uppercase text-xs tracking-widest mb-2">Descripción</h4>
                  <p className="opacity-80">{project.long_description}</p>
                </div>
                {project.tags.length > 0 && (
                  <div>
                    <h4 className="font-black text-[var(--color-rosa-vibrante)] uppercase text-xs tracking-widest mb-2">Stack Técnico</h4>
                    <p className="opacity-80">{project.tags.join(", ")}</p>
                  </div>
                )}
                {project.architecture && (
                  <div>
                    <h4 className="font-black text-[var(--color-violeta-seguridad)] uppercase text-xs tracking-widest mb-2">Arquitectura</h4>
                    <p className="opacity-80 whitespace-pre-line">{project.architecture}</p>
                  </div>
                )}
                {project.results && (
                  <div>
                    <h4 className="font-black text-[var(--color-violeta-seguridad)] uppercase text-xs tracking-widest mb-2">Resultados</h4>
                    <p className="opacity-80 whitespace-pre-line">{project.results}</p>
                  </div>
                )}
              </div>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}