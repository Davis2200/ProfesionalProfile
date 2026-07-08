# Documento de Diseño UI/UX (Data-Driven Aesthetic)
Este documento define las leyes psicológicas y los tokens técnicos que garantizan el Efecto de Estética-Usabilidad
.
A. Fundamentos de Diseño (Design Tokens)
Estilo Visual: Motion-Driven combinado con Minimalismo Suizo 2.0
. Buscamos que la complejidad del Big Data se sienta ligera y "limpia"
.
Paleta de Colores (Aurora Evolved):
Base: oklch(0.99 0.01 235) (Casi blanco azulado para tranquilidad).
Acento (Data Insight): oklch(0.70 0.25 15) (Rosa vibrante para CTAs y métricas clave)
.
Gobernanza/Seguridad: oklch(0.58 0.16 302) (Violeta para secciones de ciberseguridad)
.
Tipografía:
Titulares: Fredoka Black (Geometría amigable pero autoritaria).
Cuerpo: Nunito Regular con interlineado de 1.6 para máxima legibilidad
.
B. Aplicación de Leyes UX
Hick’s Law: Las opciones de contacto se limitan a tres canales (LinkedIn, GitHub, WhatsApp) para evitar la parálisis por exceso de elección
.
Postel’s Law: El formulario de contacto acepta cualquier formato de entrada (liberal) pero valida los datos de forma conservadora y elegante antes del envío
.
Gobernanza por Diseño (DbD): Se incluye un pequeño "Badge de Integridad" que explica cómo se manejan los datos del visitante, reforzando la Credibilidad del sistema
.
C. Estrategia Full Stack (Performance)
Arquitectura: Implementación en Next.js 15+ con carga progresiva de imágenes (Blur-up technique) para optimizar el LCP
.
Micro-interacciones: Los botones tienen un feedback de 150ms (escalado sutil de 0.98) para confirmar que la acción fue reconocida, eliminando la incertidumbre del usuario
.