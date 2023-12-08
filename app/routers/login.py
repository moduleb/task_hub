import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import get_cursor
from app.dto.user_dto import UserLoginDTO
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login",
             summary="Вход в систему",
             description=" - Требует username и password существующего пользователя, \n"
                         " - Возвращает токен доступа")

async def login(request: UserLoginDTO,
                cursor = Depends(get_cursor)):
    current_password = await UserService.get_pass(cursor, request.username)
    if not current_password:
        logging.info(f'Пользователь "{request.username}"не найден')
        raise HTTPException(401, detail="Неверный логин или пароль")

    if current_password == await AuthService.hash_pass(request.password):
        access_token = await AuthService.create_access_token(request.username)
        json_data = jsonable_encoder({"access_token": access_token, "token_type": "bearer"})
        return JSONResponse(content=json_data)
    else:
        raise HTTPException(401, detail="Неверный логин или пароль")
