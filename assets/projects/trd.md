# Resumen de la Arquitectura (High-Level Stack)
Para cumplir con los objetivos de estética-usabilidad y rendimiento, se implementará una arquitectura desacoplada
:
Frontend: Next.js 15+ (App Router) para una carga progresiva y optimización de Web Vitals
.
Backend: FastAPI (Python) para el procesamiento asíncrono de alta concurrencia y lógica de negocio
.
Base de Datos y Auth: Supabase (PostgreSQL) para persistencia de datos y gestión de identidades
.
Comunicaciones: Resend para notificaciones transaccionales y Stripe para el demo interactivo
.
Seguridad: OAuth 2.0 integrado para reducir la fricción en el Acto IV
.
2. Especificaciones del Backend (FastAPI)
El backend seguirá las mejores prácticas de modularidad y tipado fuerte
:
Estructura de Carpetas: Se adoptará un diseño basado en dominios (ej. app/api/v1/projects, app/crud, app/schemas) para facilitar el crecimiento del sistema
.
Validación de Datos: Uso exhaustivo de Pydantic v2 para garantizar que toda entrada sea saneada antes de procesarse, aplicando la Ley de Postel (entrada liberal, validación conservadora)
.
Concurrencia Asíncrona: Implementación de async def en las rutas de I/O intensivo (consultas a Supabase o llamadas a Stripe) para no bloquear el event loop
.
Inyección de Dependencias (DI): Se utilizará el sistema Depends de FastAPI para gestionar conexiones a bases de datos y requisitos de seguridad, permitiendo un código más testeable
.
3. Estrategia de Frontend (Next.js 15+)
El frontend debe materializar el Efecto de Estética-Usabilidad
:
Diseño Visual (Aurora Evolved): Implementación de colores en formato OKLCH para una visualización cromática superior y efectos de Glassmorphism en las tarjetas de proyectos
.
Optimización de Carga: Uso de Skeleton Screens y la técnica Blur-up para imágenes, asegurando un LCP < 2.5s
.
Acto I (Génesis): Animación de carga de 2.2s mediante SVG Paths auto-dibujados
.
Acto II (Bento Grid): Layout interactivo con Stagger Effect de 50ms disparado por scroll para presentar habilidades
.
4. Integraciones y Flujo de Datos
Acto III: Demo de E-commerce
Se desarrollará un flujo real donde el frontend (Next.js) se comunica con FastAPI para crear sesiones de pago en Stripe (modo test)
.
FastAPI actuará como orquestador, validando existencias y comunicándose con Supabase antes de retornar la URL de pago
.
Acto IV: Vínculo Humano y Autenticación
OAuth (Sin Fricción): Para el formulario conversacional, se ofrecerá inicio de sesión vía GitHub o LinkedIn a través de Supabase
. Esto evita que el usuario llene manualmente sus datos, aumentando la tasa de conversión
.
Envío de Correos (Resend): Una vez completado el formulario o la transacción de prueba, FastAPI disparará un evento asíncrono (usando BackgroundTasks) para enviar un correo de agradecimiento personalizado mediante Resend
.
5. Requisitos No Funcionales y Seguridad
Gobernanza por Diseño (DbD): Inclusión de un Badge de Integridad que explique de forma transparente el manejo de datos en el formulario
.
Graceful Shutdown: El backend implementará manejadores de señales para cerrar conexiones de Supabase de forma limpia durante el despliegue
.
Documentación de API: FastAPI generará automáticamente la documentación OpenAPI (Swagger), la cual se configurará para ser visible solo en entornos de desarrollo
.
Mitigación de DoS: Se debe asegurar el uso de python-multipart versión 0.0.27 o superior para evitar vulnerabilidades de CPU por headers ilimitados en la carga de archivos o formularios
.
**Gobernanza Dinámica**: Se sustituye el texto estático del badge por una carga asíncrona. El frontend debe tratar el Badge como un componente que depende de un estado de servidor (Server Component) para optimizar el SEO y la consistencia.
**Trazabilidad Legal**: El backend orquestará la validación conservadora comparando la versión enviada por el cliente contra las versiones activas en la base de datos.
.
6. Criterios de Aceptación (KPIs Técnicos)
Rendimiento: Puntuación de Lighthouse Performance ≥ 90
.
Continuidad: El reproductor de audio no debe reiniciarse al navegar entre rutas internas (manejo de estado global)
.
Fricción de Auth: El proceso de contacto mediante OAuth debe completarse en menos de 3 clics
.