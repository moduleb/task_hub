"""
CRUD API сервисы для /tasks

Все входные данные проверяются pydantic. Схемы хранятся в app.schemes
В каждой функции получаем курсор для работы с базой данных 'cursor=Depends(db.get_cursor)'
и передаем его классу для работы с базой данных 'db_service'

В конце работы функции формируем ответный словарь,
преобразуем в json и отправляем.
"""

from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.schemes.task import ErrorMessage, SuccessMessage
from app.database import DB
from app.logger import log_api
from app.schemes.task import TaskValidation, TaskResponse, TasksListResponse
from app.services.mysql import TaskService

router = APIRouter()
db_service = TaskService()
db = DB()


@router.post("/",
             summary="Создание новой задачи",
             status_code=status.HTTP_201_CREATED,
             response_description="Successful Response",
             responses={
                 409: {"model": ErrorMessage},
                 201: {"model": SuccessMessage},
             })
async def create(data: TaskValidation, cursor=Depends(db.get_cursor)) -> Response:
    """
    Создает новую задачу.\n
    Поле taskname должно быть уникальным.
    """

    log_api.debug(f'data: {data}')
    # Создаем запись в базе данных.
    await db_service.create(cursor, data)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'detail': 'Task created successfully'}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.get("/{task_id}",
            summary="Получение информации о задаче",
            response_model=TaskResponse,
            response_description="Successful Response",
            responses={
                404: {"model": ErrorMessage},
            })
async def get_one(task_id: int, cursor=Depends(db.get_cursor)) -> Response:
    """
    Получаем информацию о задаче заданным task_id.\n
    При отсутствии задачи с таким id, получим ошибку 404.
    """
    data = await db_service.get_one(cursor, task_id)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'data': data[0]}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.get("/", summary="Получение информации о всех задачах",
            status_code=status.HTTP_200_OK,
            response_description="Successful Response",
            response_model=TasksListResponse,
            responses={
                404: {"model": ErrorMessage},
            })
async def get_all(cursor=Depends(db.get_cursor)) -> Response:
    """
    Получаем информацию о всех задачах.\n
    При отсутствии задач, получим ошибку 404.
    """
    data: list = await db_service.get_all(cursor)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'data': data}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.put("/{task_id}",
            summary="Обновление задачи",
            status_code=status.HTTP_200_OK,
            response_description="Successful Response",
            responses={
                409: {"model": ErrorMessage},
                200: {"model": SuccessMessage},
            })
async def update(data: TaskValidation, task_id: int, cursor=Depends(db.get_cursor)) -> Response:
    """
    Обновляет информацию о задаче с заданным id\n
    Поле taskname обязательно и должно быть уникальным.\n
    При отсутствии задачи с таким id, получим ошибку 404
    """
    # Создаем запись в базе данных.
    await db_service.update(cursor, data, task_id)

    # Формируем response, преобразовываем в json и отправляем.
    response_data = {'detail': 'Task updated successfully'}
    json_data = jsonable_encoder(response_data)
    return JSONResponse(content=json_data)


@router.delete("/{task_id}",
               summary="Удаление задачи",
               status_code=status.HTTP_204_NO_CONTENT,
               response_description="Successful Response",
               responses={
                   404: {"model": ErrorMessage}
               })
async def delete(task_id: int, cursor=Depends(db.get_cursor)) -> None:
    """
    Удаляет задачу с заданным id.\n
    При отсутствии задачи с таким id, получим ошибку 404.
    """
    await db_service.delete(cursor, task_id)
