

from fastapi import APIRouter, Depends


from app.services.auth_service import AuthService

router = APIRouter()

# LOGOUT
@router.post("/logout", status_code=204,
             summary="Выход из системы",
             description=" - Требует токен в заголовке Authorization \n"
                         " - Деактивирует текущий токен")
async def logout(username: str = Depends(AuthService.logout)):
    pass