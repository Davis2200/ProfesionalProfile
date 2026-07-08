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

    # Normalización (Ley de Postel): Limpiamos los datos raw antes de la persistencia
    normalized_email = contact_in.raw_email.strip().lower()
    
    submission_data = {
        "raw_name": contact_in.raw_name,
        "raw_email": contact_in.raw_email,
        "normalized_email": normalized_email,
        "message": contact_in.message,
        "source_ip_hash": ip_hash,
        "oauth_provider": contact_in.oauth_provider,
        "oauth_subject": contact_in.oauth_subject,
        "status": "received"
    }

    # Inserción en Supabase usando el service_role key desde FastAPI (Seguro) [3]
    result = db.table("contact_submissions").insert(submission_data).execute()
    
    return ContactSubmissionOut(
        id=result.data["id"],
        message="¡Gracias! Tu mensaje ha sido procesado con integridad y calma."
    )