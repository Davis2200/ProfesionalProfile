"use client";
import { useState } from "react";

export default function ContactForm({ badgeId }: { badgeId: string }) {
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("sending");
    
    const formData = new FormData(e.currentTarget);
    
    // Construimos el payload con la estructura exacta que Pydantic valida en FastAPI
    const payload = {
      name: formData.get("name"),
      email: formData.get("email"),
      message: formData.get("message"), // ¡Este campo es indispensable!
      integrity_badge_version: badgeId   // Vinculación CA-6.6
    };

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/contact/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        setStatus("success");
      } else {
        // Si el backend responde con un error (ej: 422, 500)
        console.error("Error en la respuesta del servidor:", res.status);
        setStatus("error");
      }
    } catch (error) {
      console.error("Error de red al conectar con FastAPI:", error);
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <div className="p-6 text-center border border-emerald-500/30 rounded-2xl bg-emerald-500/5 text-emerald-700 font-medium animate-fade-in">
        ¡Mensaje cifrado y enviado con éxito! 🚀
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {status === "error" && (
        <div className="p-3 text-sm text-center border border-rose-500/30 rounded-xl bg-rose-500/5 text-rose-600 font-medium">
          Hubo un error al procesar el envío. Revisa la consola del backend.
        </div>
      )}

      <div>
        <label className="block text-xs font-semibold uppercase opacity-60 mb-2">Nombre Completo</label>
        <input 
          name="name" 
          placeholder="Tu nombre..." 
          required 
          className="w-full border-b-2 border-rosa-vibrante bg-transparent p-2 outline-none text-sm transition-all focus:border-opacity-100" 
        />
      </div>

      <div>
        <label className="block text-xs font-semibold uppercase opacity-60 mb-2">Correo Electrónico</label>
        <input 
          name="email" 
          type="email" 
          placeholder="email@ejemplo.com" 
          required 
          className="w-full border-b-2 border-rosa-vibrante bg-transparent p-2 outline-none text-sm transition-all" 
        />
      </div>

      <div>
        <label className="block text-xs font-semibold uppercase opacity-60 mb-2">Mensaje / Propuesta Técnica</label>
        <textarea 
          name="message" 
          placeholder="¿En qué hito o estrategia de datos trabajaremos juntos?..." 
          required 
          rows={4}
          className="w-full border-b-2 border-rosa-vibrante bg-transparent p-2 outline-none text-sm transition-all resize-none" 
        />
      </div>

      <button
        type="submit"
        disabled={status === "sending"}
        className="w-full py-3 px-6 rounded-xl bg-rosa-vibrante text-white font-semibold shadow-lg shadow-rosa-vibrante/20 transition-all hover:brightness-110 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {status === "sending" ? "Cifrando y Enviando..." : "Iniciar Conexión"}
      </button>
    </form>
  );
}