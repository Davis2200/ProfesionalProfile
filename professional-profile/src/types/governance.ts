// src/types/governance.ts
export interface IntegrityBadgeOut {
  readonly id: string;
  readonly version: string; // Ejemplo: "1.1.0"
  readonly content: string; // Texto legal (RF-6.5)
  readonly is_active: boolean;
  readonly created_at: string;
}