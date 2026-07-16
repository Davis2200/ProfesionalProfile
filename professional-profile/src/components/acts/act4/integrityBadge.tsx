import { IntegrityBadgeOut } from "@/types/governance";

interface IntegrityBadgeProps {
  badge: IntegrityBadgeOut; // Declaramos explícitamente que recibe el badge desde el servidor
}

export default function IntegrityBadge({ badge }: IntegrityBadgeProps) {
  return (
    <div className="inline-flex flex-col gap-2 p-4 border border-[var(--color-violeta-seguridad)]/30 rounded-2xl bg-[var(--color-violeta-seguridad)]/5">
      <div className="flex items-center gap-2">
        <span className="text-[var(--color-violeta-seguridad)] text-xs font-black uppercase">
          ✓ {badge.version}
        </span>
      </div>
      <p className="text-[10px] opacity-70 leading-relaxed max-w-[250px]">
        {badge.content}
      </p>
      {/* Input oculto para ser capturado por el formulario de contacto */}
      <input type="hidden" name="integrity_badge_version" value={badge.id} />
    </div>
  );
}