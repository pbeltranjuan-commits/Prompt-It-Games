import resend
import base64
import os
from app.config import get_settings

settings = get_settings()
resend.api_key = settings.RESEND_API_KEY

async def send_game_zip(to_email: str, zip_path: str, game_name: str):
    """Envia el ZIP per correu amb Resend."""
    try:
        with open(zip_path, "rb") as f:
            file_content = f.read()
        
        # Resend requereix el contingut en format Base64
        content_base64 = base64.b64encode(file_content).decode('utf-8')

        params = resend.Emails.SendParams(
            from_="onboarding@resend.dev",
            to=[to_email],
            subject=f" Assets llestos: {game_name}",
            html="<h1>El teu joc està llest per imprimir!</h1><p>Trobaràs tots els PNGs dins el ZIP adjunt.</p>",
            attachments=[
                {
                    "filename": f"{game_name.replace(' ', '_')}_assets.zip",
                    "content": content_base64
                }
            ],
        )
        email = resend.Emails.send(params)
        print(f"✅ Correu enviat a {to_email} (ID: {email.id})")
        return email
    except Exception as e:
        print(f"❌ Error enviant correu: {e}")
        raise e
