import type { Metadata } from "next";
import { Fredoka, Nunito } from "next/font/google";
import "./globals.css";

// Tipografía: Equilibrio entre amigabilidad y autoridad
const fontDisplay = Fredoka({
  subsets: ["latin"],
  weight: ["400", "600", "700"],
  variable: "--font-display",
});

const fontSans = Nunito({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-sans",
});

export const metadata: Metadata = {
  title: "David Nava Aguilar | Data & Code",
  description: "Arquitectura de Experiencias Sensoriales y Modelado de Datos",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${fontDisplay.variable} ${fontSans.variable} scroll-smooth`}>
      <body className="antialiased selection:bg-[var(--color-rosa-vibrante)] selection:text-white">
        {/* Acto II: Navegación Persistente (Jakob's Law) */}
        <header className="fixed top-0 w-full z-50 backdrop-blur-xl bg-[var(--color-glass-surface)] border-b border-[var(--color-glass-border)]">
          <nav className="container mx-auto px-6 h-16 flex items-center justify-between">
            <span className="font-display font-black text-2xl tracking-tighter">
              D<span className="text-[var(--color-rosa-vibrante)]">N</span>.
            </span>
            <ul className="flex gap-8 text-sm font-bold text-[var(--color-foreground)]">
              <li><a href="#genesis" className="hover:text-[var(--color-violeta-seguridad)] transition-colors">Inicio</a></li>
              <li><a href="#skills" className="hover:text-[var(--color-violeta-seguridad)] transition-colors">Expertise</a></li>
              <li><a href="#projects" className="hover:text-[var(--color-violeta-seguridad)] transition-colors">Evidencia</a></li>
            </ul>
          </nav>
        </header>
        
        <main>{children}</main>
      </body>
    </html>
  );
}