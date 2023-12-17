import random
import string

import pytest as pytest
from pydantic_core._pydantic_core import ValidationError

from app.schemes.task import TaskValidation

spec_chars = string.punctuation


def fake_str(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


values = [
    ('длина меньше 3', 're', ValidationError),
    ('длина больше 100', fake_str(101), ValidationError),
    ('содержит спецсимвол', fake_str(20) + spec_chars[1], ValidationError),
    ('содержит цифру', fake_str(20) + '1', None),
    ('тип int', 10, ValidationError)
]

@pytest.mark.parametrize("desc, value, result", values)
def test_dto(desc, value, result):
    try:
        TaskValidation(taskname=value)
    except ValidationError:
        assert result == ValidationError
