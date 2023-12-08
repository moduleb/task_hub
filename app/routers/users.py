from sqlite3 import Cursor

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import get_cursor
from app.dto.user_dto import UserUpdateDTO
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


# GET ONE
@router.get("/", summary="Получение информации о пользователе",
            description=" - Требует токен в заголовке Authorization \n"
                        " - Возвращает информацию о текущем пользователе: username, email, registration date")
async def get_one(cursor=Depends(get_cursor),
                  username=Depends(AuthService.verify_token)) -> Response:
    data = await UserService.get_one_by_username(cursor, username)
    json_data = jsonable_encoder({'data': data})
    return JSONResponse(content=json_data)

# UPDATE
@router.put("/",
            summary="Обновление данных пользователя",
            description=" - Требует токен в заголовке Authorization \n"
                        " - Возвращает обновленную информацию о текущем пользователе: username и email")
async def update(data: UserUpdateDTO,
                 cursor: Cursor = Depends(get_cursor),
                 username=Depends(AuthService.verify_token)) -> Response:
    data.password = await AuthService.hash_pass(data.password)
    await UserService.update(cursor, username, data)
    data = await UserService.get_one_by_username(cursor, username)
    json_data = jsonable_encoder({'data': data})
    return JSONResponse(content=json_data)


# DELETE
@router.delete("/", status_code=204,
               summary="Удаление пользователя",
               description=" - Требует токен в заголовке Authorization \n"
                           " - Удаляет пользователя из базы данных")
async def delete(cursor=Depends(get_cursor),
                 username=Depends(AuthService.verify_token)):
    await UserService.delete(cursor, username)
    await AuthService.delete(username)

