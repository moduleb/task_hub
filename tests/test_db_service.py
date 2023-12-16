# pip install pytest-asyncio
import pytest
from fastapi import HTTPException
from mysql.connector import IntegrityError



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


class TestGetAll():
    @pytest.mark.asyncio
    async def test_ok(self, cursor, db_service):
        # Arrange
        cursor_description = [
            ('id', 'description'),
            ('name', 'description')
        ]
        rows = [
            (1, 'Myname1'),
            (2, 'Myname2'),
        ]
        needed_data = [
            {
                'id': 1,
                'name': 'Myname1'
            },{
                'id': 2,
                'name': 'Myname2'
            }
        ]
        cursor.configure_mock(description=cursor_description)
        cursor.fetchall.return_value = rows
        query = 'SELECT id, taskname, description, category, creation_date FROM tasks'

        # Action
        response_data = await db_service.get_all(cursor)

        # Assert
        cursor.execute.assert_called_once_with(query)
        assert response_data == needed_data

    @pytest.mark.asyncio
    async def test_err500(self, cursor, db_service):
        # Arrange
        # Если cursor.description = None, должно быть вызвано исключение
        cursor.configure_mock(description=None)

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.get_all(cursor)
        assert e.value.status_code == 404
        assert e.value.detail == 'No tasks yet'

        # -----------------------
        # Arrange

        # Если cursor.fetchall() = None, должно быть вызвано исключение
        cursor.configure_mock(description="test")
        cursor.fetchall.return_value = None

        # Action & Assert
        with pytest.raises(HTTPException):
            await db_service.get_all(cursor)
        assert e.value.status_code == 404
        assert e.value.detail == 'No tasks yet'


class TestGetOne():
    @pytest.mark.asyncio
    async def test_ok(self, cursor, db_service):
        # Arrange
        task_id = 1
        task_name = 'MyName'
        cursor_description = [
            ('id', 'description'),
            ('name', 'description')
        ]
        rows = [(task_id, task_name)]
        needed_data = [
            {
                'id': task_id,
                'name': task_name
            }
        ]
        cursor.configure_mock(description=cursor_description)
        cursor.fetchall.return_value = rows
        query = 'SELECT id, taskname, description, category, creation_date FROM tasks ' \
                f'WHERE id = {task_id}'

        # Action
        response_data = await db_service.get_one(cursor, task_id)

        # Assert
        assert response_data == needed_data
        cursor.execute.assert_called_once_with(query)

    @pytest.mark.asyncio
    async def test_err404(self, cursor, db_service):
        # Arrange
        task_id = 1
        # Если cursor.description = None, должно быть вызвано исключение
        cursor.configure_mock(description=None)

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.get_one(cursor, task_id)
        assert e.value.status_code == 404
        assert e.value.detail == 'Task not found'

        # -----------------------
        # Arrange

        # Если cursor.fetchall() = None, должно быть вызвано исключение
        cursor.configure_mock(description="test")
        cursor.fetchall.return_value = None

        # Action & Assert
        with pytest.raises(HTTPException):
            await db_service.get_one(cursor, task_id)
        assert e.value.status_code == 404
        assert e.value.detail == 'Task not found'


class TestUpdate:
    @pytest.mark.asyncio
    async def test_update_ok(self, cursor, db_service, data):
        # Arrange
        task_id = 1
        cursor.configure_mock(rowcount=1)
        query = 'UPDATE tasks ' \
                f"SET taskname='{data.taskname}'," \
                f"description='{data.description}' " \
                f"category='{data.category}' " \
                f"WHERE id = {task_id}"

        # Action
        await db_service.update(cursor, data)

        # Assert
        cursor.execute.assert_called_once_with(query)

    @pytest.mark.asyncio
    async def test_update_err409_duplicate(self, cursor, db_service, data):
        # Arrange
        cursor.configure_mock(rowcount=1)
        cursor.execute.side_effect = IntegrityError('Duplicate error')

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.update(cursor, data)
        assert e.value.status_code == 409
        assert e.value.detail == 'Task с таким названием уже существует'

    @pytest.mark.asyncio
    async def test_update_err500(self, cursor, db_service, data):
        # Arrange
        # Устанавливаем количество удаленных строк - 0, ни одной строки не создалось. такого быть не должно
        cursor.configure_mock(rowcount=0)

        # Action & Assert
        with pytest.raises(HTTPException) as e:
            await db_service.update(cursor, data)
        assert e.value.status_code == 500