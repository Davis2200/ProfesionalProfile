// src/lib/governance.ts

// 1. Definimos la interfaz del Badge para que TypeScript sepa qué campos tiene
export interface Badge {
  id: string;
  status: 'active' | 'revoked' | 'pending';
  issuedAt: string;
  policyVersion: string;
}

/**
 * Obtiene el badge de integridad activo para cumplir con la trazabilidad legal (CA-6.6)
 * Por ahora devuelve un mock local para que el sitio compile.
 */
export async function getActiveBadge(): Promise<Badge> {
  // Simulamos un pequeño retraso de red o lectura de datos (opcional)
  // En el futuro, aquí harás un fetch() a tu backend de FastAPI o Supabase
  return {
    id: "badge-ca6.6-active-2026",
    status: "active",
    issuedAt: new Date().toISOString(),
    policyVersion: "v1.2.0"
  };
}