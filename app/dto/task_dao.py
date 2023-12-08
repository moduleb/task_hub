from fastapi import HTTPException
from mysql.connector import IntegrityError

from app.logger import log

# Тексты ошибок
read_err = "Ошибка получения информации из базы данных"
create_err = "Ошибка сохранения в базу данных"
update_err = "Ошибка обновления информации в базе данных"
delete_err = "Ошибка удаления из базы данных"
duplicate_err = "Task с таким названием уже существует"


class TaskService():
    async def get_all(self, cursor):
        query = 'SELECT id, taskname, description, category, creation_date FROM tasks'
        log.debug(f'QUERY: {query}')
        cursor.execute(query)
        tasks = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, task)) for task in tasks]
        return data



    # CREATE
    async def create(self, cursor, data):
        try:
            query = 'INSERT INTO tasks (taskname, description, category) ' \
                    f"VALUES ('{data.taskname}', '{data.description}', '{data.category}')"
            log.debug(f'QUERY: {query}')
            cursor.execute(query)
        except IntegrityError as e:
            if 'Duplicate' in str(e):
                log.debug(f"{duplicate_err}, taskname: '{data.taskname}'")
                raise HTTPException(409, detail=duplicate_err)

        except Exception as e:
            log.error(f"{create_err}: {e}")
            raise HTTPException(500, detail=create_err)



    async def get_one(self, cursor, task_id):
        query = 'SELECT id, taskname, description, category, creation_date FROM tasks ' \
                f'WHERE id = {task_id}'
        log.debug(f'QUERY: {query}')
        cursor.execute(query)
        task = cursor.fetchone()
        if task:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, task))
            return data
        else:
            raise HTTPException(status_code=404, detail="task not found")

    # DELETE
    async def delete(self, cursor, task_id):
        query = 'DELETE FROM tasks ' \
                f"WHERE id = '{task_id}'"
        log.debug(f'QUERY: {query}')
        try:
            cursor.execute(query)
        except Exception as e:
            log.error(f"{delete_err}: {e}")
            raise HTTPException(status_code=404, detail=f"{delete_err}")

    """
    async def get_one_by_taskname(cursor, taskname):
        query = 'SELECT taskname, email, registration_date FROM tasks ' \
                f"WHERE taskname = '{taskname}'"
        log.debug(f'QUERY: {query}')
        cursor.execute(query)
        task = cursor.fetchone()
        if task:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, task))
            return data
        else:
            raise HTTPException(status_code=404, detail="task not found")

    # UPDATE
    async def update(cursor, taskname, data):
        try:
            query = 'UPDATE tasks ' \
                f"SET password='{data.password}'," \
                f"email='{data.email}' " \
                f"WHERE taskname = '{taskname}'"

            log.debug(f'QUERY: {query}')
            cursor.execute(query)

        except IntegrityError as e:
            if 'Duplicate' in str(e):
                log.debug(f"task already exists '{taskname}'")
                raise HTTPException(409, detail=duplicate_err)

        except Exception as e:
            log.error(f"{create_err}: {e}")
            raise HTTPException(500, detail=create_err)
        """