from fastapi import HTTPException
from mysql.connector import IntegrityError

from app.logger import log

# Тексты ошибок
read_err = "Ошибка получения информации из базы данных"
create_err = "Ошибка сохранения в базу данных"
update_err = "Ошибка обновления информации в базе данных"
delete_err = "Ошибка удаления из базы данных"
duplicate_err = "Пользователь с таким 'username' или 'email' уже существует"


class UserService():
    @staticmethod
    async def get_all(cursor):
        query = 'SELECT username FROM users'
        cursor.execute(query)
        users = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, user)) for user in users]
        return data

    # CREATE
    @staticmethod
    async def create(cursor, data):
        try:
            query = 'INSERT INTO users (username, password, email) ' \
                    f"VALUES ('{data.username}', '{data.password}', '{data.email}')"
            cursor.execute(query)
            user_id = cursor.lastrowid
            return user_id

        except IntegrityError as e:
            if 'Duplicate' in str(e):
                log.debug(f"User already exists '{data.username}'")
                raise HTTPException(409, detail=duplicate_err)

        except Exception as e:
            log.error(f"{create_err}: {e}")
            raise HTTPException(500, detail=create_err)

    # READ
    @staticmethod
    async def get_one(cursor, user_id):
        query = 'SELECT username, email FROM users ' \
                f'WHERE id = {user_id}'
        log.debug(f'QUERY: {query}')
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, user))
            return data
        else:
            raise HTTPException(status_code=404, detail="User not found")

    @staticmethod
    async def get_one_by_username(cursor, username):
        query = 'SELECT username, email, registration_date FROM users ' \
                f"WHERE username = '{username}'"
        log.debug(f'QUERY: {query}')
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            columns = [column[0] for column in cursor.description]
            data = dict(zip(columns, user))
            return data
        else:
            raise HTTPException(status_code=404, detail="User not found")

    @staticmethod
    async def get_pass(cursor, username):
        query = 'SELECT password FROM users ' \
                f"WHERE username = '{username}'"
        log.debug(f'QUERY: {query}')
        cursor.execute(query)
        password = cursor.fetchone()
        if password:
            return password[0]
        else:
            raise HTTPException(status_code=404, detail="User not found")

    # UPDATE
    @staticmethod
    async def update(cursor, username, data):
        try:
            query = 'UPDATE users ' \
                f"SET password='{data.password}'," \
                f"email='{data.email}' " \
                f"WHERE username = '{username}'"

            log.debug(f'QUERY: {query}')
            cursor.execute(query)

        except IntegrityError as e:
            if 'Duplicate' in str(e):
                log.debug(f"User already exists '{username}'")
                raise HTTPException(409, detail=duplicate_err)

        except Exception as e:
            log.error(f"{create_err}: {e}")
            raise HTTPException(500, detail=create_err)

    # DELETE
    @staticmethod
    async def delete(cursor, username):
        query = 'DELETE FROM users ' \
                f"WHERE username = '{username}'"
        cursor.execute(query)


