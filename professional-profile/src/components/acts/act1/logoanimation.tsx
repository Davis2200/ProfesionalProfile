export default function LogoAnimation() {
  return (
    <div className="flex items-center justify-center h-full">
      <svg width="120" height="120" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Clase logo-path-draw definida en globals.css para animación de 2.2s */}
        <path 
          d="M20 20L50 80L80 20" 
          stroke="var(--color-rosa-vibrante)" 
          strokeWidth="8" 
          strokeLinecap="round" 
          className="logo-path-draw" 
        />
        <circle cx="50" cy="50" r="40" stroke="var(--color-violeta-seguridad)" strokeWidth="2" opacity="0.3" />
      </svg>
    </div>
  );
}