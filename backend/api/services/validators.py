import re
from typing import Optional
from fastapi import HTTPException, status

class ContactValidator:
    @staticmethod
    def normalize_phone(phone: Optional[str]) -> Optional[str]:
        """
        Aplica la Ley de Postel: Acepta formatos libres y extrae solo los dígitos.
        Útil para RF-6.2 (teléfonos con o sin guiones/espacios).
        """
        if not phone:
            return None
        # Eliminar todo lo que no sea dígito
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El teléfono debe contener al menos 10 dígitos para ser procesado con integridad."
            )
        return f"+{digits}" if not digits.startswith('0') else digits

    @staticmethod
    def clean_name(name: str) -> str:
        """Normaliza nombres eliminando espacios extra y capitalizando."""
        clean = " ".join(name.split()).title()
        if len(clean) < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Por favor, ingresa un nombre válido para el vínculo humano."
            )
        return clean

    @staticmethod
    def validate_integrity_consent(consent: bool):
        """Garantiza el cumplimiento de Gobernanza por Diseño (DbD)."""
        if not consent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debes aceptar el Badge de Integridad para procesar tus datos."
            )