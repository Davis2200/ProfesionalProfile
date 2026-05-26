import { notFound } from "next/navigation";
import { getProjectById } from "@/lib/servicios/project.services";
import Link from "next/link";

interface ProjectPageProps {
  readonly params: Promise<{ readonly id: string }>;
}

export default async function ProjectDetailPage({ params }: ProjectPageProps) {
  const { id } = await params;
  const project = await getProjectById(id);

  if (!project) notFound();

  // Determinamos dinámicamente si tenemos datos en la nueva estructura de fases
  const hasPhases = Array.isArray(project.phases) && project.phases.length > 0;

  return (
    <main className="min-h-screen bg-brand-bg text-brand-text pt-24 pb-20 px-6 font-sans">
      <article className="max-w-5xl mx-auto space-y-16 animate-in fade-in duration-700">
        
        {/* Cabecera y Acción Principal */}
        <header className="space-y-8">
          <Link href="/" className="text-xs font-black uppercase tracking-widest text-slate-400 hover:text-brand-action transition-colors">
            ← Volver al archivo científico
          </Link>
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div className="space-y-4">
              <span className="text-[10px] font-black uppercase tracking-[0.3em] text-brand-ethics bg-brand-ethics/10 px-4 py-1 rounded-full">
                {project.tag}
              </span>
              <h1 className="text-6xl font-black tracking-tighter leading-tight italic text-slate-900">{project.title}</h1>
            </div>
            {project.link && (
              <a href={project.link} target="_blank" rel="noopener noreferrer" className="btn-technical whitespace-nowrap">
                Ejecutar Sistema Predictivo ↗
              </a>
            )}
          </div>
        </header>

        {/* 1. El Problema (Business Understanding) */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-12 border-t border-slate-800 pt-12">
          <h2 className="text-sm font-black uppercase tracking-widest text-brand-action">El Problema de Negocio</h2>
          <div className="md:col-span-2 text-xl text-slate-600 leading-relaxed font-light">
            {project.problem}
          </div>
        </section>

        {/* 2. Resumen de Fases (Pequeñas tarjetas con descripción breve) */}
        <section className="space-y-6">
          <h2 className="text-sm font-black uppercase tracking-widest text-slate-400">
            Índice de Ejecución (CRISP-DM)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {hasPhases ? (
              project.phases.map((phase, index) => (
                <div key={phase.id || index} className="bg-slate-900/40 border border-white/5 p-4 rounded-technical flex flex-col justify-between space-y-2">
                  <div>
                    <span className="text-[9px] font-mono text-brand-action block font-bold">FASE 0{index + 1}</span>
                    <h3 className="font-bold text-xs text-white uppercase mt-1 tracking-tight line-clamp-1">{phase.name.split(":")[1] || phase.name}</h3>
                  </div>
                  <p className="text-[11px] text-shadow-slate-800 leading-snug line-clamp-2">
                    {phase.description}
                  </p>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-xs italic col-span-5">Fases de desarrollo en auditoría...</p>
            )}
          </div>
        </section>

        {/* 3. Herramientas y Resultados */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-slate-900 text-white p-10 rounded-technical border border-white/5">
            <h2 className="text-[10px] font-black uppercase tracking-widest text-brand-action mb-6">Herramientas Utilizadas</h2>
            <div className="flex flex-wrap gap-2">
              {project.tools.map(tool => (
                <span key={tool} className="text-xs font-mono bg-white/5 px-3 py-1 rounded border border-white/5 text-slate-300">{tool}</span>
              ))}
            </div>
          </div>
          <div className="bg-brand-ethics/5 border border-brand-ethics/20 p-10 rounded-technical flex flex-col justify-center">
            <h2 className="text-[10px] font-black uppercase tracking-widest text-brand-ethics mb-4">Impacto Cuantificado</h2>
            <p className="text-2xl font-bold tracking-tight text-brand-text">{project.results}</p>
          </div>
        </section>

        {/* 4. Desarrollo Profundo del Proyecto (Bloque completo y detallado debajo) */}
        {hasPhases && (
          <section className="space-y-10 border-t border-slate-800 pt-12">
            <div className="space-y-2">
              <h2 className="text-sm font-black uppercase tracking-widest text-brand-action">
                Memoria Técnica del Desarrollo
              </h2>
              <p className="text-xs text-slate-500 font-mono">
                Documentación detallada de la arquitectura, algoritmos e ingeniería aplicados
              </p>
            </div>

            <div className="space-y-8">
              {project.phases.map((phase, index) => (
                <div 
                  key={`detail-${phase.id || index}`} 
                  className="group relative bg-slate-900/20 border border-white/5 p-8 rounded-technical space-y-4 hover:border-brand-action/20 transition-all duration-300"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-white/5 pb-3">
                    <h3 className="text-base font-bold text-white tracking-tight font-mono">
                      {phase.name}
                    </h3>
                    <span className="text-[10px] font-mono bg-brand-action/10 text-brand-action px-2 py-0.5 rounded border border-brand-action/20 self-start sm:self-auto">
                      Módulo Estricto 0{index + 1}
                    </span>
                  </div>
                  <p className="text-sm text-black leading-relaxed font-light whitespace-pre-line">
                    {phase.description}
                  </p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* 5. Documentación y Cierre */}
        <footer className="border-t border-slate-800 pt-12 flex justify-center">
          {project.doc ? (
            <a href={project.doc} target="_blank" rel="noopener noreferrer" className="text-xs font-black uppercase border-b-2 border-brand-action pb-1 text-slate-300 hover:text-brand-action transition-colors">
              Descargar Documentación Completa (Google Docs)
            </a>
          ) : (
            <span className="text-xs font-bold text-slate-500 uppercase italic tracking-widest">
              Documentación en proceso de auditoría científica...
            </span>
          )}
        </footer>
      </article>
    </main>
  );
}