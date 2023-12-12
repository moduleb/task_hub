"""
Тесты класса DB (по работе с базой данных)
"""

from unittest.mock import patch

import pytest
from fastapi import HTTPException
from mysql.connector import OperationalError, IntegrityError

from app.config import config
from app.database import DB
from tests.mock import Mock


@patch('mysql.connector.connect')
def test_connect_after_init_class(mock_connect):
    """
    Проверяем, что при инициализации класса, подключаемся к DataBase
    и записываем ссылку на подключение в переменную 'db'
    """
    # Arrange
    mock = Mock(mock_connect)

    # Assert
    mock.mock_connect.assert_called_once_with(
        host=config.db.host,
        user=config.db.user_name,
        password=config.db.password,
        database=config.db.db_name,
    )
    assert mock.db_class.db == mock.mock_db


@patch('mysql.connector.connect')
def test_connect_exception(mock_connect):
    """
    Проверяем обработку ошибки при неудачной попытки соединения с database
    """

    # Arrange
    mock_connect.side_effect = Exception("Connection error")

    # Action & Assert
    with pytest.raises(HTTPException):
        DB()


@patch('mysql.connector.connect')
def test_get_cursor_ok(mock_connect):
    """
    Проверяем получение курсора в штатном режиме
    """
    # Arrange
    mock = Mock(mock_connect)

    # Action
    gen = mock.db_class.get_cursor()
    cursor = next(gen)

    # Assert
    assert cursor == mock.mock_cursor

@patch('mysql.connector.connect')
def test_get_cursor_operational_error(mock_connect):
    """
    Проверяем получение курсора в штатном режиме
    """
    # Arrange
    mock = Mock(mock_connect)
    mock.mock_db.cursor.side_effect = OperationalError("error")

    with pytest.raises(HTTPException) as e:
        gen = mock.db_class.get_cursor()
        cursor = next(gen)

@patch('mysql.connector.connect')
def test_is_connected(mock_connect):
    """
    проверяем, что при вызове метода класса __is_connected(),
    вызывается метод is_connected у объекта 'db'
    """

    # Arrange
    mock = Mock(mock_connect)
    mock.mock_db.is_connected.return_value = True

    # Action
    result = mock.db_class.is_connected()

    # Assert
    mock.mock_db.is_connected.assert_called_once()
    assert result is True


@patch('mysql.connector.connect')
def test_reconnect(mock_connect):
    """
    Проверяем, что при вызове метода класса ___reconnect(),
    вызывается метод _reconnect() у объекта 'db'
    """
    # Arrange
    mock = Mock(mock_connect)

    # Action
    mock.db_class.reconnect_(5)

    # Assert
    mock.mock_db.reconnect.assert_called_once()


@patch('mysql.connector.connect')
def test_get_cursor_when_connected(mock_connect):
    """
    Проверяем, что при получении курсора, проверяется статус подключения и выдается курсор
    """

    # Arrange
    mock = Mock(mock_connect)
    mock.mock_db.is_connected.return_value = True

    # Action
    gen = mock.db_class.get_cursor()
    cursor = next(gen)

    # Assert
    # Проверяем, что соединение проверилось
    mock.mock_db.is_connected.assert_called()

    # Проверяем, что ре-коннект не запускался
    mock.mock_db._reconnect.assert_not_called()

    # Проверяем, что вызвался объект cursor
    mock.mock_db.cursor.assert_called_once_with()

    # Проверяем получение курсора
    assert cursor == mock.mock_cursor


@patch('mysql.connector.connect')
def test_get_cursor_when_disconnected(mock_connect):
    """
    Соединение с базой данных потеряно.
    При попытке получения курсора, должно провериться соединение, попытка подключиться заново
    и исключение, если не получилось.
    """

    # Arrange
    mock = Mock(mock_connect)
    # Имитируем отсутствие соединения
    mock.mock_db.is_connected.return_value = False

    # Action & Assert
    with pytest.raises(Exception):
        try:
            # Пытаемся получить объект cursor
            gen = mock.db_class.get_cursor()
            next(gen)
        finally:
            # Проверяем, что соединение проверилось, прежде чем выдавать курсор
            mock.mock_db.is_connected.assert_called()
            # Проверяем, что запускался ре-коннект
            mock.mock_db._reconnect.assert_called_once()
