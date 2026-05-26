import { Metadata } from "next";
import Link from "next/link";
import { 
  Database, 
  Terminal, 
  Brain, 
  LineChart, 
  FileText, 
  Trophy 
} from "lucide-react";

export const metadata: Metadata = {
  title: "Ciencia y Metodología | David Nava",
  description: "Ecosistema de visualización, análisis avanzado y casos de Machine Learning."
};

const categories = [
  {
    title: "Visualización de Datos",
    description: "Storytelling científico enfocado en la toma de decisiones directivas.",
    icon: <LineChart className="text-brand-action" size={32} />,
    slug: "visualizacion"
  },
  {
    title: "Informes de Análisis",
    description: "Reportes EDA profundos con hallazgos e insights accionables.",
    icon: <FileText className="text-brand-action" size={32} />,
    slug: "informes"
  },
  {
    title: "Casos de Machine Learning",
    description: "Entrenamiento, evaluación y despliegue de modelos con código comentado.",
    icon: <Brain className="text-brand-action" size={32} />,
    slug: "ml-cases"
  },
  {
    title: "Tutoriales de Herramientas",
    description: "Guías técnicas paso a paso sobre Python, SQL y ecosistema Big Data.",
    icon: <Terminal className="text-brand-action" size={32} />,
    slug: "tutoriales"
  },
  {
    title: "Notas de Aprendizaje",
    description: "Documentación de certificaciones y evolución autodidacta constante.",
    icon: <Trophy className="text-brand-action" size={32} />,
    slug: "notas"
  }
];

export default function ScienceHubPage() {
  return (
    <main className="min-h-screen bg-brand-bg pt-32 pb-20 px-6 font-sans">
      <article className="max-w-6xl mx-auto space-y-16">
        
        {/* Cabecera del Hub */}
        <header className="space-y-4 border-b border-slate-200 pb-12">
          <div className="flex items-center gap-2 text-brand-ethics">
            <Database size={16} />
            <span className="text-[10px] font-black uppercase tracking-[0.4em]">Knowledge Transfer System</span>
          </div>
          <h1 className="text-6xl font-black tracking-tighter text-brand-text leading-tight italic">
            Ecosistema de <span className="text-brand-action">Ciencia de Datos.</span>
          </h1>
          <p className="max-w-2xl text-xl text-slate-500 font-medium leading-relaxed">
            Un compendio técnico diseñado para demostrar la versatilidad entre el rigor matemático 
            y la aplicabilidad de negocio en entornos de alta complejidad.
          </p>
        </header>

        {/* Rejilla de Categorías Diversificadas */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((cat) => (
            <Link 
              key={cat.slug} 
              href={`/ciencia/${cat.slug}`}
              className="group bg-brand-surface border border-slate-200 p-8 rounded-technical 
                         shadow-(--shadow-soft) hover:border-brand-action/40 transition-all 
                         flex flex-col justify-between space-y-8"
            >
              <div className="space-y-4">
                <div className="p-3 bg-brand-action/5 w-fit rounded-technical group-hover:scale-110 transition-transform">
                  {cat.icon}
                </div>
                <h2 className="text-2xl font-black tracking-tight text-brand-text italic">
                  {cat.title}
                </h2>
                <p className="text-sm text-slate-500 font-medium leading-relaxed">
                  {cat.description}
                </p>
              </div>
              
              <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-brand-action">
                Explorar Contenido <span>→</span>
              </div>
            </Link>
          ))}
        </section>

        {/* Sección de Compromiso (Society-in-the-loop) */}
        <footer className="bg-slate-900 text-white p-12 rounded-technical flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="space-y-2">
            <h3 className="text-xl font-bold tracking-tight italic text-brand-action">Society-in-the-loop Workflow</h3>
            <p className="text-slate-400 text-sm max-w-md">
              Cada análisis publicado aquí sigue estándares de transparencia y gobernanza ética de datos.
            </p>
          </div>
          <button className="btn-technical !bg-white !text-slate-900 border-none">
            Solicitar Auditoría Técnica
          </button>
        </footer>
      </article>
    </main>
  );
}