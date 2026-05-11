async def send_game_zip(to_email: str, zip_path: str, game_name: str):
    """
    MODE DE PROVES - NO ENVIA EMAILS REALS
    Només simula l'enviament i imprimeix logs
    """
    print("=" * 50)
    print("📧 EMAIL SIMULAT (sense domini verificat)")
    print("=" * 50)
    print(f" Destinatari: {to_email}")
    print(f"📦 Arxiu ZIP: {zip_path}")
    print(f"🎮 Joc: {game_name}")
    print("=" * 50)
    print("💡 Per activar emails reals:")
    print("   1. Ves a Resend.com")
    print("   2. Verifica un domini")
    print("   3. Actualitza aquest fitxer")
    print("=" * 50)
    
    # Retorna èxit sense intentar enviar res
    return {
        "status": "simulated",
        "message": "Email simulation complete - no real email sent"
    }
