from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import db
from app.models.task_dto import TaskDTO
from app.services.db_service import TaskService

router = APIRouter()
task_service = TaskService()


# CREATE
@router.post("/",
             summary="Создание нового задания",
             description=" - Требует токен в заголовке Authorization \n"
                         " - Возвращает обновленную информацию о текущем пользователе: username и email")
async def create(data: TaskDTO,
                 cursor=Depends(db.get_cursor)) -> Response:
    await task_service.create(cursor, data)
    response_data = {'msg': 'task created successfully'}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


# GET ONE
@router.get("/{task_id}", summary="Получение информации о задании",
            description=" - Требует токен в заголовке Authorization \n"
                        " - Возвращает информацию о текущем пользователе: username, email, registration date")
async def get_one(task_id: int = None,
                  cursor=Depends(db.get_cursor)) -> Response:
    pass
    data = await task_service.get_one(cursor, task_id)
    json_data = jsonable_encoder({'data': data})
    return JSONResponse(content=json_data)


# GET ALL
@router.get("/", summary="Получение информации о всех заданиях",
            description=" - Требует токен в заголовке Authorization \n"
                        " - Возвращает информацию о текущем пользователе: username, email, registration date")
async def get_all(cursor=Depends(db.get_cursor)) -> Response:
    pass
    data = await task_service.get_all(cursor)
    json_data = jsonable_encoder({'data': data})
    return JSONResponse(content=json_data)


# UPDATE
@router.put("/",
            summary="Обновление данных задания",
            description=" - Требует токен в заголовке Authorization \n"
                        " - Возвращает обновленную информацию о текущем пользователе: username и email")
async def update(data: TaskDTO,
                 cursor=Depends(db.get_cursor)) -> Response:
    pass
    # data.password = await AuthService.hash_pass(data.password)
    # await UserService.update(cursor, username, data)
    # data = await UserService.get_one_by_username(cursor, username)
    # json_data = jsonable_encoder({'data': data})
    # return JSONResponse(content=json_data)


# DELETE
@router.delete("/{task_id}",
               summary="Удаление задании",
               description=" - Требует токен в заголовке Authorization \n"
                           " - Удаляет задании из базы данных")
async def delete(task_id: int = None,
                 cursor=Depends(db.get_cursor)):
    await task_service.get_one(cursor, task_id)
    await task_service.delete(cursor, task_id)
    response_data = {'msg': 'task deleted successfully'}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)
