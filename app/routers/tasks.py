"""
CRUD API сервисы для /tasks

Все входные данные проверяются pydantic. Схемы хранятся в app.models
В каждой функции получаем курсор для работы с базой данных 'cursor=Depends(db.get_cursor)'
и передаем его классу для работы с базой данных 'db_service'

В конце работы функции формируем ответный словарь,
преобразуем в json и отправляем.
"""

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import DB
from app.models.task_dto import TaskDTO
from app.services.mysql import TaskService

router = APIRouter()
db_service = TaskService()
db = DB()


@router.post("/",
             summary="Создание нового задания",
             description=" - Требует токен в заголовке Authorization \n"
                         " - Возвращает обновленную")
async def create(data: TaskDTO, cursor=Depends(db.get_cursor)) -> Response:
    """
    При удачном добавлении записи db_service ничего не вернет.
    При исключении, сам отправит HTTP ошибку.
    """
    # Создаем запись в базе данных.
    await db_service.create(cursor, data)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'msg': 'task created successfully'}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.get("/{task_id}",
            summary="Получение информации о задании",
            description=" - Требует токен в заголовке Authorization \n"
                        " - Возвращает информацию о текущем ")
async def get_one(task_id: int, cursor=Depends(db.get_cursor)) -> Response:
    """
    Получаем запись из базы данных с полученным task_id.
    При удачном добавлении записи db_service ничего не вернет.
    При исключении, сам отправит HTTP ошибку.
    """
    data = await db_service.get_one(cursor, task_id)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'data': data}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.get("/", summary="Получение информации о всех заданиях",
            description=" - Требует токен в заголовке Authorization \n"
                        " - Возвращает информацию о текущем п")
async def get_all(cursor=Depends(db.get_cursor)) -> Response:
    """
    Получаем все записи из базы данных.
    При удачном поиске db_service вернет список словарей в формате
    [{taskname: str, description: str, category: str, creation_date: datatime}, {...}]
    Если ничего не найдет, пришлет пустой список.
    """
    data: list = await db_service.get_all(cursor)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'data': data}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.put("/",
             summary="Создание нового задания",
             description=" - Требует токен в заголовке Authorization \n"
                         " - Возвращает обновленную")
async def update(data: TaskDTO, cursor=Depends(db.get_cursor)) -> Response:
    """
    При удачном добавлении записи db_service ничего не вернет.
    При исключении, сам отправит HTTP ошибку.
    """
    # Создаем запись в базе данных.
    await db_service.update(cursor, data)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'msg': 'task updated successfully'}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.delete("/{task_id}",
               summary="Удаление задании",
               description=" - Требует токен в заголовке Authorization \n"
                           " - Удаляет задании из базы данных")
async def delete(task_id: int, cursor=Depends(db.get_cursor)) -> Response:
    # await db_service.get_one(cursor, task_id)
    """
    Удаляем запись с полученным task_id из базы данных.
    При удачном удалении записи db_service ничего не вернет.
    При исключении, сам отправит HTTP ошибку.
    """
    await db_service.delete(cursor, task_id)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'msg': 'Task deleted successfully'}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)
