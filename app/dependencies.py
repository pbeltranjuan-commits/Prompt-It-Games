from fastapi import Depends, HTTPException, Header
from typing import Optional

async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> str:
    """
    Obtenir l'usuari actual del token JWT.
    
    TODO: Implementar validació JWT real amb python-jose o PyJWT
    Per ara, retorna un user_id dummy per a desenvolupament.
    """
    if not authorization:
        # Per a desenvolupament, permetem accés sense token
        # raise HTTPException(status_code=401, detail="No token provided")
        return "user_dev_123"
    
    # Aquí aniria la validació real del token JWT
    # Exemple:
    # try:
    #     payload = jwt.decode(authorization.replace("Bearer ", ""), JWT_SECRET, algorithms=["HS256"])
    #     return payload["sub"]
    # except:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    
    return "user_from_token"
