import Link from 'next/link';

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[var(--color-glass-border)] bg-[var(--color-fondo-tranquilo)]/80 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        {/* Logo con animación - Acto I */}
        <Link href="/" className="font-display text-2xl font-black tracking-tighter logo-path-draw">
          D<span className="text-[var(--color-rosa-vibrante)]">N</span>.
        </Link>

        {/* Navegación Estándar - Jakob's Law */}
        <nav className="hidden md:flex gap-8 text-sm font-bold uppercase tracking-widest">
          <Link href="#inicio" className="hover:text-[var(--color-rosa-vibrante)] transition-colors">Inicio</Link>
          <Link href="#habilidades" className="hover:text-[var(--color-rosa-vibrante)] transition-colors">Habilidades</Link>
          <Link href="#proyectos" className="hover:text-[var(--color-rosa-vibrante)] transition-colors">Proyectos</Link>
          <Link href="#contacto" className="hover:text-[var(--color-rosa-vibrante)] transition-colors">Contacto</Link>
        </nav>

        {/* Hick's Law: 3 opciones máximas de contacto */}
        <div className="flex gap-4">
          <a href="#" className="btn-action min-h-[44px] px-6 text-xs" style={{padding: '0.5rem 1rem'}}>LinkedIn</a>
        </div>
      </div>
    </header>
  );
}