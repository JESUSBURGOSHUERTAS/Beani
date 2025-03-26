import requests
from app.models.user import User
from app.services.auth_service import create_user
from app.core.config import settings

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

async def google_auth(code: str):
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_info = response.json()
    
    if "access_token" not in token_info:
        return None

    user_info = requests.get(GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {token_info['access_token']}"}).json()
    
    user = await User.find_one(User.email == user_info["email"])
    if not user:
        user = await create_user(email=user_info["email"], password="", full_name=user_info.get("name"))

    return user
