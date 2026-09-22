import stripe
from typing import List
from fastapi import HTTPException
from ..core.config import settings
from ..schemas.stripe_demo import CheckoutSessionOut

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    async def create_checkout_session(
        items: List[dict], 
        user_email: str
    ) -> CheckoutSessionOut:
        """
        Crea una sesión de pago en modo test.
        Implementa el flujo real solicitado en RF-4.4.
        """
        try:
            line_items = [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item["name"]},
                        "unit_amount": int(item["price"] * 100), # Stripe usa centavos
                    },
                    "quantity": 1,
                } for item in items
            ]

            # Definimos la URL base de tu frontend de forma segura
            frontend_url = "https://davidnava.vercel.app"

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"{frontend_url}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{frontend_url}/?canceled=true",
                customer_email=user_email,
                metadata={"source": "The Tranquil Journey Portfolio"}
            )
            
            return CheckoutSessionOut(
                checkout_url=session.url,
                session_id=session.id
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en la pasarela de Stripe: {str(e)}")