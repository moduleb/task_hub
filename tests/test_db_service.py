# pip install pytest-asyncio
import pytest
from fastapi import HTTPException
from mysql.connector import IntegrityError

from app.services.mysql import TaskService


class TestDelete:
    @pytest.mark.asyncio
    async def test_delete_ok(self, cursor, db_service):

        # Arrange
        task_id = 1
        cursor.configure_mock(rowcount=1)
        query = 'DELETE FROM tasks WHERE id = %s', task_id

        # Action
        await db_service.delete(cursor, task_id)

        # Assert
        cursor.execute.assert_called_once_with(query)

    @pytest.mark.asyncio
    async def test_delete_err404(self, cursor, db_service):
        # Arrange
        task_id = 1
        # Устанавливаем количество удаленных строк (значит запись с таким task_id не найдена
        cursor.configure_mock(rowcount=0)

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.delete(cursor, task_id)
        assert e.value.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_err500(self, cursor, db_service):
        # Arrange
        task_id = 1
        # Устанавливаем количество удаленных строк - 2, значит удалилось две строки. такого быть не должно
        cursor.configure_mock(rowcount=2)

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.delete(cursor, task_id)
        assert e.value.status_code == 500

class TestCreate:
    @pytest.mark.asyncio
    async def test_create_ok(self, cursor, db_service, data):

        # Arrange
        cursor.configure_mock(rowcount=1)
        query = 'INSERT INTO tasks (taskname, description, category) ' \
                f"VALUES ('{data.taskname}', '{data.description}', '{data.category}')"

        # Action
        await db_service.create(cursor, data)

        # Assert
        cursor.execute.assert_called_once_with(query)


    @pytest.mark.asyncio
    async def test_create_err409_duplicate(self, cursor, db_service, data):
        # Arrange
        cursor.configure_mock(rowcount=1)
        cursor.execute.side_effect = IntegrityError('Duplicate error')

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.create(cursor, data)
        assert e.value.status_code == 409
        assert e.value.detail == 'Task с таким названием уже существует'

    @pytest.mark.asyncio
    async def test_create_err500(self, cursor, db_service, data):
        # Arrange
        # Устанавливаем количество удаленных строк - 0, ни одной строки не создалось. такого быть не должно
        cursor.configure_mock(rowcount=0)

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.create(cursor, data)
        assert e.value.status_code == 500


