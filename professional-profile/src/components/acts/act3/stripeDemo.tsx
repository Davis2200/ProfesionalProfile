"use client";
import { useState } from "react";

export default function StripeDemo() {
  const [loading, setLoading] = useState(false);

  const handleTestCheckout = async () => {
    setLoading(true);
    try {
      // Flujo real: Next.js -> FastAPI -> Stripe Test [4]
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/demo/checkout`, { method: 'POST' });
      const { url } = await res.json();
      if (url) window.location.href = url;
    } catch (e) {
      console.error("Error en el flujo de datos", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card border-dashed border-[var(--color-violeta-seguridad)] flex flex-col items-center text-center">
      <div className="mb-4 p-4 rounded-full bg-[var(--color-violeta-seguridad)]/10 text-[var(--color-violeta-seguridad)]">
        💳
      </div>
      <h3 className="text-xl mb-2">Sandbox de E-commerce</h3>
      <p className="text-sm opacity-70 mb-6 max-w-xs">
        Presiona para ver cómo FastAPI orquesta una sesión de Stripe y retorna el flujo al frontend.
      </p>
      <button 
        onClick={handleTestCheckout}
        disabled={loading}
        className="btn-action bg-[var(--color-violeta-seguridad)] hover:bg-[var(--color-violeta-seguridad)]/90"
      >
        {loading ? "Orquestando..." : "Ejecutar Flujo de Datos"}
      </button>
    </div>
  );
}