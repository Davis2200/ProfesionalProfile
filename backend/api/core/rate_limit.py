from fastapi import Request, HTTPException, status
import time
from typing import Dict

# Nota: Para producción escalable, se recomienda usar Redis.
# Esta implementación en memoria es adecuada para el MVP inicial del portafolio.

class RateLimiter:
    def __init__(self, requests_limit: int, window_seconds: int):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.client_state: Dict[str, list] = {}

    async def __call__(self, request: Request):
        # Usamos el hash de la IP o el ID del usuario si está autenticado (Acto IV)
        client_ip = request.client.host
        current_time = time.time()
        
        if client_ip not in self.client_state:
            self.client_state[client_ip] = []
            
        # Limpiar ventanas antiguas
        self.client_state[client_ip] = [
            t for t in self.client_state[client_ip] 
            if current_time - t < self.window_seconds
        ]
        
        if len(self.client_state[client_ip]) >= self.requests_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiadas solicitudes. 'The Tranquil Journey' requiere calma."
            )
            
        self.client_state[client_ip].append(current_time)

# Instancias específicas para diferentes RFs
# Límite estricto para el formulario de contacto (Postel's Law) [10]
contact_rate_limiter = RateLimiter(requests_limit=3, window_seconds=60)
# Límite para el demo de Stripe (Acto III) [11]
stripe_demo_limiter = RateLimiter(requests_limit=5, window_seconds=60)