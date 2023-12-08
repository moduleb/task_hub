from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import get_cursor
from app.dto.user_dto import UserRegDTO
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


# REGISTER
@router.post("/register",
             summary="Регистрация пользователя",
             description=" - Создает пользователя в базе данных \n"
                         " - Возвращает токен доступа")
async def create(request: UserRegDTO, cursor = Depends(get_cursor)) -> Response:

    request.password = await AuthService.hash_pass(request.password)
    user_id = await UserService.create(cursor, request)
    user_data = await UserService.get_one(cursor, user_id)

    access_token = await AuthService.create_access_token(user_data['username'])
    data = {'data': user_data, "access_token": access_token, "token_type": "bearer"}
    json_data = jsonable_encoder(data)
    return JSONResponse(content=json_data)
