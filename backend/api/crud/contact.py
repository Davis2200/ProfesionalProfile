import hashlib
from supabase import Client
from ..schemas.contact import ContactSubmissionCreate, ContactSubmissionOut

async def create_contact_submission(
    db: Client, 
    contact_in: ContactSubmissionCreate,
    client_ip: str
) -> ContactSubmissionOut:
    """
    Registra un contacto aplicando Minimización de Datos (DbD) [3].
    No guardamos la IP en claro, sino un hash para trazabilidad anónima.
    """
    # Anonimización de IP por diseño (DbD) [1]
    ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()

    # Normalización (Ley de Postel): Leemos desde '.email' de Pydantic limpiando los datos raw
    normalized_email = contact_in.email.strip().lower()
    
    # IMPORTANTE: Aquí mapeamos las propiedades limpias de tu Pydantic 
    # hacia los nombres de columnas exactos de tus tablas en Supabase.
    submission_data = {
        "raw_full_name": contact_in.name,          # 👈 AGREGA ESTA LÍNEA (Resuelve la restricción NOT NULL)
        "full_name": contact_in.name,              # Columna en Postgres: full_name
        "email": normalized_email,                 # Columna en Postgres: email
        "message": contact_in.message,             # Columna en Postgres: message
        "source_ip_hash": ip_hash,                 # Columna en Postgres: source_ip_hash
        "status": "pending",                       # Status por defecto
        "integrity_badge_version": str(contact_in.integrity_badge_version) # ID del Badge
    }

    # Inserción en Supabase usando el service_role key desde FastAPI (Seguro) [3]
    result = db.table("contact_submissions").insert(submission_data).execute()
    
    # Obtenemos la primera fila insertada retornada por la API de Supabase
    inserted_row = result.data[0] if result.data else {}
    
    return ContactSubmissionOut(
        id=str(inserted_row.get("id", "")),
        name=inserted_row.get("full_name", contact_in.name),
        email=inserted_row.get("email", normalized_email),
        message=inserted_row.get("message", contact_in.message),
        created_at=inserted_row.get("created_at")
    )