import { Metadata } from "next";
import Link from "next/link";
import { 
  Database, 
  Terminal, 
  Trophy, 
  Bike, 
  Compass, 
  BrainCircuit,
  FileBadge 
} from "lucide-react";

export const metadata: Metadata = {
  title: "Perfil Profesional | David Nava",
  description: "Científico de Datos especialista en Gobernanza y Analytics con enfoque de negocio."
};

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-brand-bg pt-32 pb-20 px-6 font-sans">
      <article className="max-w-5xl mx-auto space-y-20 animate-in fade-in duration-700">
        
        {/* Cabecera Técnica */}
        <header className="space-y-6">
          <div className="flex items-center gap-2 text-brand-ethics">
            <FileBadge size={16} />
            <span className="text-[10px] font-black uppercase tracking-[0.4em]">Society-in-the-loop Practitioner</span>
          </div>
          <h1 className="text-6xl font-black tracking-tighter text-brand-text leading-tight italic">
            Científico de Datos en Formación | <span className="text-brand-action underline decoration-brand-action/20">Gobernanza & Analytics</span>
          </h1>
        </header>

        {/* Sección 1: Propuesta de Valor (Pitch) */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center border-y border-slate-200 py-16">
          <div className="space-y-6">
            <h2 className="text-sm font-black uppercase tracking-widest text-brand-action">Propuesta de Valor</h2>
            <p className="text-2xl text-slate-600 font-medium leading-tight">
              Actualmente curso el sexto semestre en el <span className="text-brand-text font-black">IPN</span>, 
              diseñando soluciones que aseguran la <span className="text-brand-text font-black underline decoration-brand-ethics/40 text-brand-ethics">Gobernanza</span> y utilidad de la información.
            </p>
          </div>
          <div className="bg-brand-surface border border-slate-200 p-8 rounded-technical shadow-(--shadow-soft)">
            <p className="text-slate-500 leading-relaxed italic">
              "Mi enfoque es el ciclo de vida del dato bajo estándares <span className="font-bold text-brand-text">ISO 8000 / ISO 25012</span>, 
              cerrando la brecha entre el rigor técnico y la estrategia empresarial."
            </p>
          </div>
        </section>

        {/* Sección 2: Experiencia e Impacto */}
        <section className="space-y-12">
          <div className="flex justify-between items-end">
            <h2 className="text-sm font-black uppercase tracking-widest text-brand-action">Experiencia y Logros</h2>
            <span className="text-xs font-mono text-slate-400">2+ Años en Conduent Solutions</span>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Logro en Conduent */}
            <div className="md:col-span-2 bg-slate-900 text-white p-10 rounded-technical flex flex-col justify-between space-y-8">
              <p className="text-xl font-medium leading-relaxed">
                Logré transformar reportes operativos en <span className="text-brand-action font-black uppercase tracking-tighter">Diagnósticos Accionables</span>, 
                asegurando la continuidad operativa mediante automatización avanzada.
              </p>
              <div className="flex flex-wrap gap-3">
                {["Python", "SQL", "Power BI", "Apache Spark", "Docker"].map((tech) => (
                  <span key={tech} className="text-[10px] font-mono bg-white/10 px-3 py-1 rounded border border-white/10">
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            {/* Métrica Destacada */}
            <div className="bg-brand-ethics/5 border border-brand-ethics/20 p-10 rounded-technical flex flex-col justify-center text-center">
              <p className="text-5xl font-black text-brand-ethics tracking-tighter">80%</p>
              <p className="text-xs font-black uppercase tracking-widest mt-2 text-brand-text">Precisión en Clustering</p>
              <p className="text-[10px] text-slate-500 mt-4 uppercase">Caso: Manzanas Prósperas</p>
            </div>
          </div>
        </section>

        {/* Sección 4: El Toque Humano (Más allá de los datos) */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8 border-t border-slate-200 pt-16">
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="p-4 bg-brand-action/10 rounded-full text-brand-action"><Trophy size={24} /></div>
            <h3 className="text-xs font-black uppercase tracking-widest">Logros</h3>
            <p className="text-sm text-slate-500 px-4">Disciplina y resiliencia en equipos de alto rendimiento desde los 18 años.</p>
          </div>
          <div className="flex flex-col items-center text-center space-y-4 border-x border-slate-100">
            <div className="p-4 bg-brand-action/10 rounded-full text-brand-action"><Bike size={24} /></div>
            <h3 className="text-xs font-black uppercase tracking-widest">Outdoor</h3>
            <p className="text-sm text-slate-500 px-4">Ciclismo y senderismo para abordar problemas complejos desde nuevas perspectivas.</p>
          </div>
          <div className="flex flex-col items-center text-center space-y-4">
            <div className="p-4 bg-brand-action/10 rounded-full text-brand-action"><BrainCircuit size={24} /></div>
            <h3 className="text-xs font-black uppercase tracking-widest">Curiosidad</h3>
            <p className="text-sm text-slate-500 px-4">Combustible constante analizando papers y experimentando con nuevos frameworks.</p>
          </div>
        </section>

        {/* CTAs Finales */}
        <footer className="pt-10 flex flex-col md:flex-row gap-4 justify-center">
          <Link href="/#proyectos" className="btn-technical">
            Ver mis Proyectos Científicos
          </Link>
          <a href="/cv-david-nava.pdf" className="btn-technical !bg-brand-text !shadow-brand-text/10">
            Descargar CV Actualizado (PDF)
          </a>
        </footer>
      </article>
    </main>
  );
}