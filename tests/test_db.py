import pytest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from app.database import DB

from app.config import config


@patch('mysql.connector.connect')
def test_connect_after_init_class(mock_connect: MagicMock):
    """
    Проверяем, что при инициализации класса, подключаемся к DataBase
    и записываем ссылку на подключение в переменную 'db'
    """
    # Arrange
    mock_db = MagicMock()
    mock_connect.return_value = mock_db

    # Создаем экземпляр класса
    db = DB()

    # Assert
    mock_connect.assert_called_once_with(
        host=config.db.HOST,
        user=config.db.USER_NAME,
        password=config.db.PASSWORD,
        database=config.db.DB_NAME,
    )
    assert db.db == mock_db


@patch('mysql.connector.connect')
def test_connect_exception(mock_connect):
    """
    Проверяем обработку ошибки при неудачной попытки соединения с database
    """

    # Arrange
    mock_connect.side_effect = Exception("Connection error")

    # Act & Assert
    with pytest.raises(HTTPException):
        db = DB()

@patch('mysql.connector.connect')
def test_is_connected(mock_connect):
    """
    проверяем, что при вызове метода класса __is_connected(),
    вызывается метод is_connected у объекта 'db'
    """
    # Arrange
    mock_db = MagicMock()
    mock_connect.return_value = mock_db
    mock_db.is_connected.return_value = True
    db = DB()

    # Act
    result = db._DB__is_connected()

    # Assert
    mock_db.is_connected.assert_called_once()
    assert result == True

@patch('mysql.connector.connect')
def test_reconnect(mock_connect):
    """
    Проверяем, что при вызове метода класса __reconnect(),
    вызывается метод reconnect() у объекта 'db'
    """
    # Arrange
    mock_db = MagicMock()
    mock_connect.return_value = mock_db
    db = DB()

    # Act
    db._DB__reconnect(5)

    # Assert
    mock_db.reconnect.assert_called_once()


values = [True, False]
@pytest.mark.parametrize('value',values)
@patch('mysql.connector.connect')
def test_get_cursor(mock_connect, value):
    """
    Проверяем, что при получении курсора, проверяется статус подключения и пере-подключается при разрыве
    """

    # Arrange
    mock_db = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor
    db = DB()

    # Статус соединение с базой данных True (соединено)
    mock_db.is_connected.return_value = True

    # Пытаемся получить объект курсор
    gen = db.get_cursor()
    cursor = next(gen)
    # Проверяем, что соединение проверилось
    mock_db.is_connected.assert_called()
    # Проверяем, что реконнект не запускался
    mock_db.reconnect.assert_not_called()
    # Проверяем, что вызвался объект cursor
    mock_db.cursor.assert_called_once_with()
    # Проверяем получение курсора
    assert cursor == mock_cursor

    # Статус соединение с базой данных False (нет соединения)
    mock_db.is_connected.return_value = False
    # При потере соединения возникнет исключение
    with pytest.raises(Exception):
        # Пытаемся получить объект cursor
        gen = db.get_cursor()
        next(gen)
        # Проверяем, что соединение проверилось, прежде чем выдавать курсок
        mock_db.is_connected.assert_called()
        # Проверяем, что запускался реконнект
        mock_db.reconnect.assert_called_once()



