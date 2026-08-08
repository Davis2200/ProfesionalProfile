"use client";
import { useState, useEffect } from 'react';

export default function WelcomeModal() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Mostrar el modal solo al cargar la primera vez
    const hasVisited = sessionStorage.getItem('welcome_shown');
    if (!hasVisited) {
      setIsOpen(true);
    }
  }, []);

  const handleChoice = (startWithMusic: boolean) => {
    setIsOpen(false);
    sessionStorage.setItem('welcome_shown', 'true');

    if (startWithMusic) {
      // Buscamos el botón del reproductor flotante y le damos clic programáticamente
      const playButton = document.querySelector('button[aria-label="Reproducir música"], button[aria-label="Pausar música"]') as HTMLButtonElement;
      if (playButton) {
        playButton.click();
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white rounded-2xl p-6 md:p-8 max-w-md w-full shadow-2xl border border-gray-100 text-center flex flex-col items-center">
        
        <div className="w-16 h-16 bg-[var(--color-rosa-vibrante)]/10 text-[var(--color-rosa-vibrante)] rounded-full flex items-center justify-center text-3xl mb-4 shadow-inner">
          🏀
        </div>

        <h2 className="text-xl md:text-2xl font-bold font-display text-gray-900 mb-2">
          ¡Bienvenido a mi Portafolio!
        </h2>
        
        <p className="text-gray-600 text-sm mb-6 leading-relaxed">
          Diseñé este espacio combinando ingeniería de software y desarrollo web. ¿Te gustaría recorrerlo con música ambiental de fondo?
        </p>

        <div className="flex flex-col sm:flex-row gap-3 w-full">
          <button
            onClick={() => handleChoice(true)}
            className="flex-1 bg-[var(--color-rosa-vibrante)] text-white font-medium py-3 px-4 rounded-xl shadow-md hover:opacity-90 active:scale-95 transition-all text-sm cursor-pointer flex items-center justify-center gap-2"
          >
            <span>▶</span> Sí, con música
          </button>
          
          <button
            onClick={() => handleChoice(false)}
            className="flex-1 bg-gray-100 text-gray-700 font-medium py-3 px-4 rounded-xl hover:bg-gray-200 active:scale-95 transition-all text-sm cursor-pointer"
          >
            Explorar en silencio
          </button>
        </div>
      </div>
    </div>
  );
}