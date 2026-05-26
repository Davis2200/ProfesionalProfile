import "./globals.css";
import { Inter } from "next/font/google";
import { Navbar } from "@/components/organisms/navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "David Nava | Data Scientist con Enfoque Ético",
  description: "Arquitecto de soluciones de ciencia de datos impulsado por la innovación y la responsabilidad humana.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className="scroll-smooth">
      <body className={`${inter.className} bg-brand-dark text-slate-200 antialiased`}>
        <Navbar />
        {children}
      </body>
    </html>
  );
}