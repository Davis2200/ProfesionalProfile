"use client";
import { useState, useEffect, useRef } from 'react';

interface Track {
  id: string;
  title: string;
  artist: string;
  audio_url: string;
  cover_url: string;
}

export default function AudioPlayer() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    async function fetchTracksFromApi() {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/tracks/`);
        if (!res.ok) throw new Error("Error al obtener las pistas");
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          setTracks(data);
        }
      } catch (err) {
        console.error("Fallo al conectar con el backend:", err);
      }
    }
    fetchTracksFromApi();
  }, []);

  const currentTrack = tracks[currentIndex];

  const togglePlay = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play().then(() => {
        setIsPlaying(true);
      }).catch((err) => {
        console.error("Error al reproducir audio:", err);
      });
    }
  };

  const handleNextTrack = () => {
    const nextIndex = (currentIndex + 1) % tracks.length;
    setCurrentIndex(nextIndex);
    // Reproducir automáticamente la siguiente pista si ya estaba activo el reproductor
    setTimeout(() => {
      if (audioRef.current && isPlaying) {
        audioRef.current.play().catch(() => setIsPlaying(false));
      }
    }, 100);
  };

  if (tracks.length === 0) return null;

  return (
    <div className="fixed bottom-8 left-8 z-50 flex items-center gap-4 py-3 px-6 rounded-full shadow-lg bg-white/70 backdrop-blur-md border border-white/20">
      <audio ref={audioRef} src={currentTrack?.audio_url} onEnded={handleNextTrack} />

      <div className="flex items-center gap-3">
        {/* Cover con animación giratoria si está reproduciendo */}
        <div className="w-10 h-10 rounded-full overflow-hidden border border-white/30 shadow-sm">
          <img 
            src={currentTrack.cover_url} 
            alt="Cover" 
            className={`w-full h-full object-cover ${isPlaying ? 'animate-spin-slow' : ''}`} 
          />
        </div>

        <div className="flex flex-col max-w-[130px] md:max-w-[180px]">
          <span className="text-[10px] uppercase font-black tracking-tighter opacity-60">Now Playing</span>
          <span className="text-xs font-bold font-display truncate">{currentTrack?.title}</span>
          <span className="text-[10px] opacity-70 truncate">{currentTrack?.artist}</span>
        </div>
      </div>
      
      {/* Botón interactivo con el balón de básquet */}
      <button 
        onClick={togglePlay}
        className="w-11 h-11 flex items-center justify-center rounded-full bg-[var(--color-rosa-vibrante)] text-white overflow-hidden active:scale-95 transition-transform shadow-md relative group cursor-pointer"
        aria-label={isPlaying ? "Pausar música" : "Reproducir música"}
      >
        <span>🏀</span>
        
        <div className="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-xs font-bold">
          {isPlaying ? '⏸' : '▶'}
        </div>
      </button>

      <style jsx global>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .animate-spin-slow {
          animation: spin-slow 8s linear infinite;
        }
      `}</style>
    </div>
  );
}