import base64
from app.config import get_settings

settings = get_settings()

async def send_game_zip(to_email: str, zip_path: str, game_name: str):
    """
    MODE DE PROVES: No envia email real
    Només genera el ZIP i imprimeix info
    """
    print(f"📧 EMAIL SIMULAT (mode proves)")
    print(f"📧 Destinatari: {to_email}")
    print(f"📦 ZIP generat: {zip_path}")
    print(f"🎮 Joc: {game_name}")
    print(f"💡 NOTA: Per enviar emails reals, necessites:")
    print(f"   1. Un domini verificat a Resend.com")
    print(f"   2. O utilitzar un servei alternatiu")
    
    # Retorna èxit sense enviar res
    return {"status": "simulated", "message": "Email simulation complete"}
