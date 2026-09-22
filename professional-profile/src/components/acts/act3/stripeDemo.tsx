"use client";
import { useState } from "react";

export default function StripeDemo() {
  const [loading, setLoading] = useState(false);

  const handleTestCheckout = async () => {
    setLoading(true);
    try {
      const requestBody = {
        product_ids: ["prod_demo_123"],
        success_url: `${window.location.origin}/?success=true`,
        cancel_url: `${window.location.origin}/?canceled=true`
      };
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/projects/checkout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });
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