"use client";
import { useState } from "react";
import ProjectCard from "./projctCard"; // Importamos tu tarjeta (con tu nombre exacto)
import DeepDiveModal from "./deepDivemodal"; // Importamos tu modal
import StripeDemo from "./stripeDemo"; // Importamos tu Sandbox

// Debe coincidir con el schema ProjectCardOut del backend (FastAPI)
interface Project {
  title: string;
  slug: string;
  short_description: string;
  thumbnail_url?: string | null;
  glass_intensity: number;
  tags: string[];
}

interface ProjectsSectionProps {
  projects: Project[];
}

export default function ProjectsSection({ projects }: ProjectsSectionProps) {
  // Guardamos solo el slug del proyecto seleccionado; el modal jala el detalle completo a la API
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null);

  return (
    <div className="flex flex-col gap-12">
      {/* Grid para las tarjetas y el demo */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch">

        {/* Renderizamos todos los proyectos que vienen de la BD */}
        {projects.map((project) => (
          <ProjectCard
            key={project.slug}
            title={project.title}
            description={project.short_description}
            tags={project.tags}
            onClick={() => setSelectedSlug(project.slug)}
          />
        ))}

        {/* Añadimos tu Sandbox de Stripe como una tarjeta más al final */}
        <StripeDemo />

      </div>

      {/* Modal que se muestra solo si hay un proyecto seleccionado; carga el deep dive por slug */}
      <DeepDiveModal
        isOpen={!!selectedSlug}
        onClose={() => setSelectedSlug(null)}
        slug={selectedSlug}
      />
    </div>
  );
}