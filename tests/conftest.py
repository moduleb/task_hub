from unittest import mock
import os

import pytest
from unittest.mock import MagicMock

from app.models.task_dto import TaskDTO
from app.services.mysql import TaskService


@pytest.fixture
def cursor():
    return MagicMock()

@pytest.fixture
def data():
    return TaskDTO(
        taskname='Task 1',
        description='Description 1',
        category='Category 1'
    )

@pytest.fixture
def db_service():
    return TaskService()

