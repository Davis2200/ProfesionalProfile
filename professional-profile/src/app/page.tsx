import { Hero } from "@/components/organisms/hero";
import { ProjectCard } from "@/components/molecules/projectcard";
import { getAllProjects } from "@/lib/servicios/project.services";
import { IProject } from "@/models/proyectos";

export default async function Home() {
  // Fetching directo en el servidor (RSC) para máxima velocidad de carga (TTFB)
  const projects: IProject[] = await getAllProjects();

  return (
    <main className="relative pt-20"> 
      <Hero 
        title="David Nava Aguilar"
        subtitle="Junior Data Scientist | IPN | Soluciones Basadas en Datos"
        description="Construyo sistemas que cierran la brecha entre el rigor científico y la aplicabilidad empresarial, priorizando siempre la ética y la transparencia."
      />

      <section id="proyectos" className="max-w-6xl mx-auto px-6 py-24 border-t border-white/5">
        <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-4">
          <div>
            <h2 className="text-sm uppercase tracking-[0.4em] text-brand-ethics font-black mb-2">
              Evidencia de Evolución
            </h2>
            <p className="text-3xl font-bold text-black tracking-tight">Proyectos Destacados</p>
          </div>
          <button className="text-xs font-bold uppercase tracking-widest text-slate-400 hover:text-brand-action transition-colors">
            Ver archivo completo →
          </button>
        </div>

        {/* Renderizado Dinámico Resiliente */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              id={project.id}
              title={project.title}
              metric={project.metric}
              description={project.description}
              tag={project.tag}
            />
          ))}
        </div>
      </section>

      <section id="etica" className="max-w-4xl mx-auto px-6 py-24 text-center">
        <h2 className="text-4xl font-black mb-6 text-black">
          Ciencia de Datos con <span className="text-brand-ethics">Propósito.</span>
        </h2>
        <p className="text-slate-400 leading-relaxed text-lg italic">
          "Mi objetivo no es solo crear modelos matemáticamente sólidos, sino sistemas de datos 
          que sean accionables, responsables y orientados al bienestar humano."
        </p>
      </section>
    </main>
  );
}