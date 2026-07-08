# Backend Schema — Portafolio "The Tranquil Journey"

Basado en `trd.md`, `prd.md` y `flujo.md`. Arquitectura desacoplada:
**Next.js 15+ (frontend)** ⇄ **FastAPI (backend)** ⇄ **Supabase/PostgreSQL** (+ Stripe test, Resend).

## Contenido de este entregable

```
portfolio-backend-schema/
├── database/
│   └── schema.sql          # DDL completo para Supabase (tablas, enums, RLS, triggers)
├── app/
│   └── schemas/             # Pydantic v2 — capa de validación de FastAPI
│       ├── content.py        # RF-1 Hero rotativo, RF-5 personal/audio
│       ├── skill.py           # RF-3 Bento Grid + Miller's Law
│       ├── project.py         # RF-4 Proyectos + Deep Dive
│       ├── stripe_demo.py     # RF-4.4 Demo e-commerce sandbox
│       └── contact.py         # RF-6 Formulario + Postel's Law + Badge de Integridad
└── README.md
```

## Estructura recomendada del backend completo (app/)

Siguiendo TRD §2 ("diseño basado en dominios"):

```
app/
├── main.py                     # instancia FastAPI, middlewares, CORS, lifespan (graceful shutdown)
├── core/
│   ├── config.py               # settings (Pydantic Settings), env vars
│   ├── security.py             # OAuth2 / Supabase JWT verification
│   └── rate_limit.py           # mitigación DoS (slowapi o similar)
├── db/
│   ├── session.py              # cliente Supabase / engine async SQLAlchemy
│   └── deps.py                 # Depends() para conexión DB
├── schemas/                    # <- entregado en este paquete
│   ├── content.py
│   ├── skill.py
│   ├── project.py
│   ├── stripe_demo.py
│   └── contact.py
├── crud/                       # capa de acceso a datos por dominio
│   ├── skills.py
│   ├── projects.py
│   ├── stripe_demo.py
│   └── contact.py
├── services/
│   ├── stripe_service.py        # crea Checkout Sessions en modo test
│   ├── resend_service.py        # BackgroundTasks -> email de agradecimiento
│   └── validators.py            # normalización teléfono/email (Postel's Law)
└── api/
    └── v1/
        ├── hero.py               # GET /api/v1/hero
        ├── skills.py             # GET /api/v1/skills
        ├── projects.py           # GET /api/v1/projects, GET /api/v1/projects/{slug}
        ├── stripe_demo.py        # POST /api/v1/checkout/session
        ├── contact.py            # POST /api/v1/contact
        └── integrity.py          # GET /api/v1/integrity-badge
```

## Endpoints principales sugeridos (RESTful, versión v1)

| Método | Ruta | Dominio | RF |
|---|---|---|---|
| GET | `/api/v1/hero` | Titulares rotativos | RF-1.3 |
| GET | `/api/v1/skills` | Bento Grid con items anidados | RF-3 |
| GET | `/api/v1/projects` | Listado de tarjetas (`ProjectCardOut`) | RF-4.1 |
| GET | `/api/v1/projects/{slug}` | Deep Dive (`ProjectDeepDiveOut`) | RF-4.3 |
| GET | `/api/v1/demo/products` | Productos del demo Stripe | RF-4.4 |
| POST | `/api/v1/demo/checkout` | Crea `CheckoutSessionCreate` → Stripe test | RF-4.4, CA-4 |
| POST | `/api/v1/stripe/webhook` | Webhook de confirmación de pago (async) | RF-4.4 |
| GET | `/api/v1/audio-tracks` | Pistas del mini-player | RF-5.1 |
| GET | `/api/v1/integrity-badge` | Texto del Badge de Integridad | RF-6.4 |
| POST | `/api/v1/contact` | `ContactSubmissionCreate` → validación conservadora | RF-6 |

## Decisiones de diseño clave

1. **Postel's Law aplicada en dos capas**: el frontend acepta formato libre (teléfono,
   nombre), y `ContactSubmissionCreate` normaliza y valida antes de tocar la base de
   datos. Se guardan tanto los valores `raw_*` como los normalizados, para trazabilidad
   y para poder ajustar reglas de normalización sin perder el dato original.

2. **Miller's Law reforzada en dos capas**: un trigger de PostgreSQL (`fn_enforce_millers_law`)
   y un `field_validator` en Pydantic (`SkillBlockOut`) — así el límite de 9 items por
   bloque no depende únicamente de la disciplina del frontend.

3. **Minimización de datos (Governance by Design)**: no se almacena IP en claro
   (`source_ip_hash`), y el fingerprint de analítica/checkout es anónimo, sin PII.
   El Badge de Integridad (`integrity_badge_content`) es versionado para poder
   auditar qué texto vio el usuario al dar su consentimiento.

4. **RLS en Supabase**: las tablas de contenido (hero, skills, projects, productos,
   audio) tienen lectura pública vía `anon key`. Las tablas transaccionales
   (`contact_submissions`, `demo_orders`, `analytics_events`) solo se escriben desde
   FastAPI usando el `service_role key`, nunca directo desde el navegador — esto es
   lo que hace segura la validación "conservadora" del lado del servidor.

5. **Demo Stripe como flujo real, no mockeado**: `demo_orders`/`demo_order_items`
   persisten cada intento, permitiendo reconciliar contra los webhooks de Stripe
   test y demostrar en vivo el flujo Next.js → FastAPI → Stripe → Supabase (CA-4).

## Siguientes pasos sugeridos

- Generar los módulos `crud/*.py` que envuelvan estas tablas con el cliente de Supabase.
- Definir `services/stripe_service.py` para crear/confirmar Checkout Sessions en modo test.
- Configurar Supabase Auth (OAuth GitHub/LinkedIn) y mapear `oauth_provider`/`oauth_subject`
  en `contact_submissions` cuando el visitante decida autenticarse en vez de llenar el
  formulario manualmente (TRD Acto IV, "Sin Fricción").