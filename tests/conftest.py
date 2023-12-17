from unittest import mock
import os

import pytest
from unittest.mock import MagicMock

from app.schemes.task import TaskValidation
from app.services.mysql import TaskService


@pytest.fixture
def cursor():
    return MagicMock()

@pytest.fixture
def data():
    return TaskValidation(
        taskname='Task 1',
        description='Description 1',
        category='Category 1'
    )

@pytest.fixture
def db_service():
    return TaskService()

