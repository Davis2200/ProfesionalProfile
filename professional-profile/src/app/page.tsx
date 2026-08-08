import { Suspense } from "react";
import Hero from "@/components/acts/act1/hero";
import SkeletonHero from "@/components/acts/act1/skeletonHero";
import BentoGrid from "@/components/acts/act2/bentoGrid";
import ProjectsSection from "@/components/acts/act3/projectSection"; 
import ContactForm from "@/components/acts/act4/contactForm";
import IntegrityBadge from "@/components/acts/act4/integrityBadge";
import { IntegrityBadgeOut } from "@/types/governance";

// Debe coincidir con el schema ProjectCardOut del backend (FastAPI)
export interface ProjectCard {
  title: string;
  slug: string;
  short_description: string;
  thumbnail_url?: string | null;
  glass_intensity: number;
  tags: string[];
}

// 1. Función para obtener los proyectos directamente desde la API de FastAPI
async function getProjects(): Promise<ProjectCard[]> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/projects/`, {
    next: { tags: ['projects'] }
  });
  if (!res.ok) throw new Error("Error cargando proyectos");
  return res.json();
}

// 2. Función centralizada en el servidor para el badge
async function getActiveBadge(): Promise<IntegrityBadgeOut> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/integrity-badge/`, {
    next: { tags: ['governance'] } 
  });
  if (!res.ok) throw new Error("Error cargando Badge de Integridad");
  return res.json();
}

export default async function Home() {
  // Cargamos los datos en el servidor antes de renderizar
  const badge = await getActiveBadge();
  const projects = await getProjects();

  return (
    <div className="relative w-full">
      {/* Acto I: La Génesis */}
      <section id="inicio" className="min-h-screen">
        <Suspense fallback={<SkeletonHero />}>
          <Hero />
        </Suspense>
      </section>

      {/* Acto II: La Tríada del Conocimiento */}
      <section id="habilidades" className="py-24 px-4 bg-fondo-tranquilo">
        <div className="container mx-auto">
          <h2 className="text-4xl md:text-5xl font-display mb-12 text-center">
            Dominios <span className="text-rosa-vibrante">Técnicos</span>
          </h2>
          <BentoGrid />
        </div>
      </section>

      {/* Acto III: Catálogo de Soluciones (Proyectos) */}
      <section id="proyectos" className="py-24 px-4 bg-fondo-tranquilo">
        <div className="container mx-auto">
          <h2 className="text-4xl md:text-5xl font-display mb-12 text-center">
            Proyectos <span className="text-rosa-vibrante">Destacados</span>
          </h2>
          
          {/* Renderizamos el contenedor pasándole los proyectos de la BD */}
          <ProjectsSection projects={projects} />
          
        </div>
      </section>

      {/* Acto IV: El Vínculo Humano y Cierre */}
      <section id="contacto" className="py-24 px-4 bg-white">
        <div className="container mx-auto max-w-4xl">
          <div className="grid md:grid-cols-2 gap-12 items-start">
            <div>
              <h2 className="text-4xl font-display mb-6">Hablemos.</h2>
              <p className="mb-8 opacity-70">
                Diseñemos juntos el próximo hito en tu estrategia de datos.
              </p>
              
              <IntegrityBadge badge={badge} />
            </div>

            <ContactForm badgeId={badge.id} />
          </div>
        </div>
      </section>
    </div>
  );
}