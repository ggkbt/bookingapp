from typing import List

from fastapi import APIRouter, Form, HTTPException, Header
from keycloak import KeycloakOpenID

from booking_service.settings import settings

keycloak_router = APIRouter(tags=['Auth'])

user_token = ""
keycloak_openid = KeycloakOpenID(server_url=settings.keycloak_url,
                                 client_id=settings.keycloak_client_id,
                                 realm_name=settings.keycloak_realm,
                                 client_secret_key=settings.keycloak_client_secret)


@keycloak_router.post("/get_token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(username=username,
                                      password=password,
                                      grant_type="password")
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def get_user_roles(token: str) -> List[str]:
    token_info = keycloak_openid.introspect(token)
    if not token_info['active']:
        raise HTTPException(status_code=401, detail="Inactive or invalid token")

    roles = token_info.get('resource_access', {}).get(settings.keycloak_client_id, {}).get('roles', [])
    return roles


def require_role(required_roles: List[str]):
    def role_validator(token: str = Header(...)):
        user_roles = get_user_roles(token)
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(status_code=403, detail="Permission denied")
        return True

    return role_validator
