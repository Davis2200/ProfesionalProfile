import type { Metadata } from "next";
import { Fredoka, Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/layout/header";
import AudioPlayer from "@/components/layout/audio_player";
import { cn } from "@/lib/utils";
import WelcomeModal from "@/components/layout/welcome_modal";

// Configuración de tipografía según TRD
const fontDisplay = Fredoka({ subsets: ["latin"], variable: "--font-display" });
const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "David Nava Aguilar | Data & Code",
  description: "Arquitectura de Experiencias Sensoriales y Modelado de Datos",
};

// Función asíncrona interna para recuperar de forma segura la versión del Badge activo
async function getActiveBadgeId(): Promise<string> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/integrity-badge`, {
      next: { tags: ["governance"] } // Etiqueta para revalidación bajo demanda
    });
    if (!res.ok) return "";
    const data = await res.json();
    return data.id; // Retorna el UUID requerido para la trazabilidad de consentimiento
  } catch {
    return ""; // Fallback elegante en caso de que el backend esté apagado temporalmente
  }
}

// Convertimos RootLayout a async para poder usar await arriba
export default async function RootLayout({ children }: { readonly children: React.ReactNode }) {
  const badgeId = await getActiveBadgeId();

  return (
    <html lang="es" className={cn("scroll-smooth", "font-sans", inter.variable)}>
      <body className={`${fontDisplay.variable} ${inter.variable} font-sans antialiased bg-[oklch(0.99_0.01_235)] text-[var(--color-foreground)]`}>
        <Header />
        
        
        {/* El contenido dinámico de tus páginas */}
        <main>{children}</main>
        
        {/* El reproductor de audio se mantiene al final para persistencia sonora global */}
        <AudioPlayer /><WelcomeModal/>
      </body>
    </html>
  );
}