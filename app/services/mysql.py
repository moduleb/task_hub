"""
Модуль взаимодействия с базой данный Mysql
"""
from typing import List, Dict, Any

from mysql.connector import IntegrityError
from mysql.connector.cursor import CursorBase
from starlette.exceptions import HTTPException

from app.logger import db_log
from app.models.task_dto import TaskDTO


class TaskService:
    """
    Класс для взаимодействия с базой данных Mysql.
    """

    def __init__(self):
        db_log.debug('Class TaskService init process...')

    @staticmethod
    async def create(cursor: CursorBase, data: TaskDTO) -> None:
        """
        Создает одну запись в базе данных.
        """
        try:
            query = 'INSERT INTO tasks (taskname, description, category) ' \
                    f"VALUES ('{data.taskname}', '{data.description}', '{data.category}')"

            db_log.debug('QUERY: %s', query)
            cursor.execute(query)

        except IntegrityError as e:
            if 'Duplicate' in str(e):
                db_log.debug('Task с таким названием уже существует: %s', e)
                raise HTTPException(409, detail='Task с таким названием уже существует') from e

        # Проверяем количество удаленных строк, если удалилась 1, то все ок
        rowcount = cursor.rowcount

        db_log.debug('Количество созданных строк в базе данных: %s', rowcount)

        if rowcount != 1:
            db_log.debug('Количество созданных строк на равно 1')
            raise HTTPException(500, detail='Unknown database error')

    async def get_all(self, cursor: CursorBase) -> List[Dict[str, Any]]:
        """
        Возвращает все найденные записи в таблице 'tasks'
        """
        query = 'SELECT id, taskname, description, category, creation_date FROM tasks'

        db_log.debug('QUERY: %s', query)
        cursor.execute(query)
        rows = cursor.fetchall()


        if rows and cursor.description is not None:
            # Получаем заголовки столбцов
            columns = [column[0] for column in cursor.description]
        else:
            db_log.debug("Table 'tasks' is empty")
            raise HTTPException(404, detail='No tasks yet')

        # Соединяем заголовки с их значениями построчно и возвращаем
        data = [dict(zip(columns, row)) for row in rows]
        return data


    async def get_one(self, cursor: CursorBase, task_id: int) -> List[Dict[str, Any]]:
        """
        Возвращает одну запись с заданным 'task_id'.
        """

        query = 'SELECT id, taskname, description, category, creation_date FROM tasks ' \
                f'WHERE id = {task_id}'

        db_log.debug('QUERY: %s', query)
        cursor.execute(query)

        rows = cursor.fetchall()
        if rows and cursor.description is not None:
            # Получаем заголовки столбцов
            columns = [column[0] for column in cursor.description]
        else:
            db_log.debug("Task not found, task_id: %s", task_id)
            raise HTTPException(404, detail='Task not found')

        # Соединяем заголовки с их значениями построчно
        data = [dict(zip(columns, row)) for row in rows]
        return data

    @staticmethod
    async def delete(cursor: CursorBase, task_id: int) -> None:
        """
        Удаляет одну запись с заданным 'task_id'.
        """
        query = f'DELETE FROM tasks WHERE id = {task_id}'

        db_log.debug('QUERY: %s', query)
        cursor.execute(query)

        # Проверяем количество удаленных строк, если удалилась 1, то все ок
        rowcount = cursor.rowcount

        db_log.debug('Количество удаленных строк из базы данных: %s', rowcount)

        if rowcount == 0:
            db_log.debug("Task not found, task_id: %s", task_id)
            raise HTTPException(404, detail='Task not found')

        if rowcount != 1:
            db_log.debug('Количество обновленных строк на равно 1')
            raise HTTPException(500, detail='Unknown database error')

    @staticmethod
    async def update(cursor: CursorBase, data: TaskDTO, task_id: int) -> None:
        """
        Обновляет одну запись в базе данных.
        """
        try:
            query = 'UPDATE tasks ' \
                    f"SET taskname='{data.taskname}', " \
                    f"description='{data.description}', " \
                    f"category='{data.category}' " \
                    f"WHERE id = {task_id}"

            db_log.debug('QUERY: %s', query)
            cursor.execute(query)

        except IntegrityError as e:
            if 'Duplicate' in str(e):
                db_log.debug('Task с таким названием уже существует: %s', e)
                raise HTTPException(409, detail='Task already exist') from e

        # Проверяем количество удаленных строк, если изменилась 1, то все ок
        rowcount = cursor.rowcount
        db_log.debug('Количество обновленных строк в базе данных: %s', rowcount)

        if cursor.rowcount != 1:
            db_log.debug('Количество обновленных строк на равно 1')
            raise HTTPException(400, detail='Задач обновлено: 0')
