# Product Requirements Document (PRD)
## Portafolio Profesional Interactivo — "The Tranquil Journey"

| | |
|---|---|
| **Versión** | 1.0 |
| **Autor** | Product Owner & Requirements Architect |
| **Fecha** | Julio 2026 |
| **Estado** | Draft para revisión de stakeholders |
| **Fuentes** | `diseño_ui_ux.md`, `flujo.md` |

---

## 1. Contexto y Problema

### 1.1 Antecedentes
El propietario del producto es un profesional con un perfil híbrido (Modelado Predictivo, Gobernanza de Datos y Desarrollo Full Stack). El mercado de portafolios técnicos está saturado de plantillas genéricas (CV en HTML, grids de proyectos sin narrativa) que no logran comunicar profundidad técnica ni generar confianza suficiente para iniciar una conversación comercial o de reclutamiento.

### 1.2 El Dolor Real del Usuario
Existen dos usuarios con dolores distintos:

- **Reclutadores / Stakeholders técnicos**: necesitan validar en segundos si el candidato tiene profundidad real (no solo buzzwords) en Data Science y Full Stack, sin leer un CV extenso.
- **El propietario del portafolio (dueño de producto)**: necesita un activo digital que funcione como "vendedor 24/7", capaz de transmitir las tres fortalezas (Predictivo, Gobernanza, Full Stack) sin saturar cognitivamente al visitante (parálisis por exceso de elección) y sin sacrificar percepción de calidad técnica.

### 1.3 Oportunidad
Aplicar el **Efecto de Estética-Usabilidad** (interfaces bellas se perciben como más usables y confiables) combinado con leyes UX comprobadas (Hick's, Jakob's, Miller's, Fitts's, Postel's) para convertir el asombro visual en una acción de conversión medible (contacto).

---

## 2. Objetivos y KPIs

### 2.1 Objetivos de Producto
1. Comunicar en menos de 5 segundos las tres fortalezas del perfil (Modelado Predictivo, Gobernanza de Datos, Desarrollo Full Stack).
2. Generar confianza suficiente para que el visitante complete el formulario de contacto o inicie conversación por un canal directo.
3. Demostrar competencia técnica real mediante artefactos interactivos (no solo texto), en particular el demo de e-commerce con Stripe.

### 2.2 KPIs (Métricas de Éxito)

| KPI | Métrica | Meta (Target) | Herramienta de medición |
|---|---|---|---|
| Engagement inicial | % de scroll hasta Acto II (Habilidades) | > 60% | Mixpanel / Hotjar |
| Percepción de carga | LCP (Largest Contentful Paint) | < 2.5s | Lighthouse / Web Vitals |
| Interés técnico | Clicks en tarjetas de proyecto (Deep Dive) | > 25% de visitantes | Hotjar / Analytics |
| Conversión de contacto | Tasa de envío de formulario / visitas únicas | > 4% | Analytics + backend logs |
| Calidad de leads | Formularios válidos tras validación conservadora | > 90% de los enviados | Backend / SQL |
| Fricción de interacción | Tasa de error en formulario (Postel's Law) | < 5% | Analytics de formulario |
| Retención de atención | Tiempo promedio en sitio | > 90s | Analytics |

---

## 3. User Stories

Formato: **Como** [rol], **quiero** [acción], **para** [beneficio].

### Acto I — Génesis (Carga y Hero)
- **US-01**: Como visitante, quiero ver una animación de carga elegante (logo dibujándose), para percibir que el sitio es cuidado y profesional desde el primer instante.
- **US-02**: Como visitante, quiero que el contenido debajo del hero cargue en segundo plano (skeleton screen), para no sentir tiempos muertos de espera.
- **US-03**: Como visitante, quiero ver un titular que rote entre las tres fortalezas del perfil, para entender rápidamente el rango de expertise sin necesidad de scrollear.

### Acto II — Tríada del Conocimiento (Habilidades)
- **US-04**: Como visitante, quiero encontrar la navegación en la posición habitual (menú superior), para no perder tiempo aprendiendo una interfaz nueva.
- **US-05**: Como visitante, quiero ver las habilidades organizadas en un grid tipo Bento Box, para escanear visualmente las categorías sin sobrecarga de información.
- **US-06**: Como visitante, quiero que los algoritmos (DBSCAN, K-Means, etc.) aparezcan de forma escalonada al hacer scroll, para procesar la información en bloques manejables.

### Acto III — Evidencia Técnica (Proyectos)
- **US-07**: Como visitante técnico, quiero interactuar con tarjetas de proyecto con efecto glassmorphism, para percibir un nivel de ejecución visual superior al promedio.
- **US-08**: Como visitante, quiero hacer clic en una tarjeta y ver un "Deep Dive" del proyecto, para validar la profundidad técnica real detrás de cada trabajo.
- **US-09**: Como reclutador o cliente potencial, quiero ver un demo interactivo de e-commerce con Stripe, para comprobar en vivo el flujo de datos entre Next.js y FastAPI.

### Acto IV — Vínculo Humano y Cierre
- **US-10**: Como visitante, quiero conocer un poco del lado personal del propietario (básquet, música), para generar una conexión humana más allá de lo técnico.
- **US-11**: Como visitante, quiero escuchar un reproductor de audio integrado sin que se interrumpa mi navegación, para tener una experiencia continua y sin fricciones.
- **US-12**: Como visitante interesado, quiero completar un formulario conversacional simple, para contactar al propietario dejando una sensación final de control y satisfacción.
- **US-13**: Como visitante preocupado por su privacidad, quiero ver un "Badge de Integridad" que explique el manejo de mis datos, para confiar en enviar mi información de contacto.

---

## 4. Requisitos Funcionales

### RF-1 Sistema de Carga y Hero (Acto I)
- RF-1.1: El logo debe renderizarse como animación SVG path (auto-dibujado) con duración de **2.2s**.
- RF-1.2: El resto del contenido debe cargar en paralelo usando **Skeleton Screens** (no spinners genéricos).
- RF-1.3: El titular del Hero debe rotar dinámicamente entre 3 strings: "Modelado Predictivo", "Gobernanza de Datos", "Desarrollo Full Stack" (carrusel de texto, transición suave).
- RF-1.4: El fondo del Hero debe implementar el efecto visual "Aurora UI" con la paleta definida en la sección 6.

### RF-2 Navegación (Jakob's Law)
- RF-2.1: Menú de navegación persistente (sticky) en la parte superior en todos los breakpoints.
- RF-2.2: La estructura de navegación debe seguir convenciones estándar de la industria (Inicio / Habilidades / Proyectos / Sobre mí / Contacto).

### RF-3 Sección de Habilidades (Acto II)
- RF-3.1: Layout tipo **Bento Box Grid**, responsive (reflow a columna única en mobile).
- RF-3.2: Cada tarjeta de habilidad/algoritmo debe aparecer con **Stagger Effect** de 50ms entre elementos, disparado por scroll (Intersection Observer).
- RF-3.3: Agrupación de habilidades limitada a categorías cognitivamente manejables (Miller's Law: máximo 7±2 elementos visibles por bloque).

### RF-4 Sección de Proyectos (Acto III)
- RF-4.1: Tarjetas de proyecto con efecto **Glassmorphism** (blur + transparencia + borde sutil).
- RF-4.2: Todas las áreas clickeables deben tener un tamaño mínimo de **44x44px** (Fitts's Law).
- RF-4.3: Al hacer clic en una tarjeta, debe abrirse una vista "Deep Dive" (modal o página de detalle) con: descripción técnica, stack utilizado, arquitectura y resultados.
- RF-4.4: Debe existir un componente interactivo (demo) de e-commerce conectado a Stripe (modo sandbox/test), visualizando el flujo de datos entre Next.js (frontend) y FastAPI (backend).

### RF-5 Sección Personal y Cierre (Acto IV)
- RF-5.1: Reproductor de audio embebido con controles persistentes (mini-player) que no se detiene al navegar entre secciones (continuidad espacial vía estado global o `position: sticky`/Web Audio API).
- RF-5.2: Sección personal debe incluir referencias a intereses (básquet, música) de forma minimalista (íconos + texto breve, sin saturar).

### RF-6 Formulario de Contacto
- RF-6.1: Formulario conversacional (estilo chat/paso a paso), aplicando el **Peak-End Rule** — el último paso debe incluir una confirmación visual satisfactoria (animación de éxito).
- RF-6.2: **Postel's Law** — el campo de entrada debe aceptar formatos libres (ej. número de teléfono con o sin guiones, nombre con o sin apellido), pero la validación backend debe ser estricta antes de aceptar el envío.
- RF-6.3: Los canales de contacto alternativos deben limitarse a **3 opciones** (LinkedIn, GitHub, WhatsApp) — aplicación directa de **Hick's Law**.
- RF-6.4: Debe mostrarse un **Badge de Integridad** (Governance by Design) visible cerca del formulario, con texto explicando cómo se procesan y almacenan los datos del visitante.

### RF-7 Micro-interacciones
- RF-7.1: Todos los botones deben tener feedback táctil de **150ms** (escala 0.98) al presionar/hacer clic.
- RF-7.2: Las transiciones de estado (hover, focus, active) deben ser consistentes en todo el sitio.

---

## 5. Requisitos No Funcionales

| Categoría | Requisito |
|---|---|
| **Rendimiento** | LCP < 2.5s mediante carga progresiva de imágenes (técnica Blur-up). Uso de Next.js 15+ con App Router y optimización de imágenes nativa. |
| **Escalabilidad** | Arquitectura desacoplada Next.js (frontend) + FastAPI (backend) para permitir escalado independiente de servicios de datos/ML. |
| **Seguridad** | Validación conservadora de todo input de formulario en backend (sanitización, rate limiting). Transacciones Stripe únicamente en modo test/sandbox para el demo. |
| **Accesibilidad** | Contraste de color conforme a WCAG AA sobre la paleta Aurora Evolved. Todos los elementos interactivos navegables por teclado. Tamaño mínimo de touch target 44px (ya cubierto en RF-4.2). |
| **Responsividad** | Diseño mobile-first; Bento Grid y Glassmorphism deben degradar correctamente en viewports pequeños. |
| **Compatibilidad** | Soporte en las últimas 2 versiones de Chrome, Safari, Firefox y Edge. |
| **Mantenibilidad** | Componentes reutilizables documentados (Storybook opcional) para tokens de diseño (colores OKLCH, tipografía). |
| **Privacidad** | Cumplimiento con principios de Governance by Design: minimización de datos recolectados en el formulario y comunicación clara de su uso (Badge de Integridad). |

---

## 6. Especificación de Diseño (Design Tokens — referencia)

| Token | Valor | Uso |
|---|---|---|
| Color base | `oklch(0.99 0.01 235)` | Fondo general |
| Color acento (Data Insight) | `oklch(0.70 0.25 15)` | CTAs, métricas clave |
| Color gobernanza | `oklch(0.58 0.16 302)` | Secciones de ciberseguridad/datos |
| Tipografía titulares | Fredoka Black | H1-H3 |
| Tipografía cuerpo | Nunito Regular, line-height 1.6 | Párrafos |

---

## 7. Criterios de Aceptación

### CA-1 — Hero y Carga (US-01, US-02, US-03)
- [ ] La animación del logo se completa en 2.2s ± 100ms sin bloquear la carga del resto del contenido.
- [ ] El skeleton screen desaparece únicamente cuando el contenido real está listo para renderizar.
- [ ] El titular rotativo cicla las 3 frases sin saltos ni parpadeos (CLS = 0 en esa zona).

### CA-2 — Navegación (US-04)
- [ ] El menú permanece visible (sticky) en scroll hacia abajo y hacia arriba en desktop y mobile.

### CA-3 — Habilidades (US-05, US-06)
- [ ] El grid Bento Box se reorganiza correctamente en 3 breakpoints (desktop, tablet, mobile) sin overlaps.
- [ ] El stagger effect dispara únicamente cuando el bloque entra en viewport (no en la carga inicial completa).

### CA-4 — Proyectos (US-07, US-08, US-09)
- [ ] Todas las tarjetas responden a hover/click con el efecto glassmorphism visible.
- [ ] El área clickeable de cada tarjeta mide como mínimo 44x44px, verificable en devtools.
- [ ] El Deep Dive abre en menos de 300ms tras el clic.
- [ ] El demo de Stripe procesa una transacción de prueba end-to-end (Next.js → FastAPI → Stripe test mode) sin errores.

### CA-5 — Sección Personal (US-10, US-11)
- [ ] El audio continúa reproduciéndose al navegar entre secciones/rutas internas sin reiniciarse.

### CA-6 — Formulario y Cierre (US-12, US-13)
- [ ] El formulario acepta al menos 3 variantes de formato de entrada válidas por campo (ej. teléfono) y las normaliza correctamente en backend.
- [ ] Un envío con datos inválidos es rechazado con mensaje de error claro, sin perder los datos ya ingresados por el usuario.
- [ ] Al completar el envío exitoso, se muestra una confirmación con refuerzo positivo (Peak-End Rule).
- [ ] Se muestran exactamente 3 canales de contacto alternativos: LinkedIn, GitHub, WhatsApp.
- [ ] El Badge de Integridad es visible sin necesidad de scroll adicional en la sección de contacto.

### CA-7 — Rendimiento
- [ ] Lighthouse Performance Score ≥ 90 en desktop y ≥ 80 en mobile.
- [ ] LCP < 2.5s medido con datos de campo (CrUX) o Web Vitals en producción.

---

## 8. Fuera de Alcance (Out of Scope) — v1.0
- Sistema de autenticación de usuarios/visitantes.
- Blog o sistema de gestión de contenido (CMS) editorial.
- Internacionalización (i18n) multi-idioma.
- Panel de administración para editar contenido del portafolio sin código.

---

## 9. Priorización (MoSCoW)

| Requisito | Prioridad |
|---|---|
| Hero, navegación, formulario de contacto básico | **Must have** |
| Bento Grid + Stagger effect | **Must have** |
| Glassmorphism + Deep Dive de proyectos | **Must have** |
| Demo interactivo Stripe/FastAPI | **Should have** |
| Reproductor de audio persistente | **Should have** |
| Badge de Integridad | **Should have** |
| Animación de logo SVG (2.2s) | **Could have** |
| Micro-interacciones de 150ms en todos los botones | **Could have** |

---

## 10. Riesgos y Dependencias

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Complejidad del demo Stripe + FastAPI puede retrasar el timeline | Alto | Priorizar como "Should have" y usar modo sandbox desde el día 1 |
| Animaciones (SVG, stagger, glassmorphism) pueden degradar performance en mobile de gama baja | Medio | Testing en dispositivos reales de gama media/baja antes de release |
| Reproductor de audio persistente puede generar conflictos de estado en navegación SPA | Medio | Usar Context API o librería de estado global desde el diseño inicial |

---

## 11. Anexo — Trazabilidad Flujo → Requisito

| Acto (flujo.md) | Requisitos Funcionales | User Stories |
|---|---|---|
| Acto I: La Génesis | RF-1 | US-01, US-02, US-03 |
| Acto II: Tríada del Conocimiento | RF-2, RF-3 | US-04, US-05, US-06 |
| Acto III: Evidencia Técnica | RF-4 | US-07, US-08, US-09 |
| Acto IV: Vínculo Humano y Cierre | RF-5, RF-6 | US-10, US-11, US-12, US-13 |