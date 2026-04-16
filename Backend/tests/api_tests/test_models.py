import pytest
from api.api_models.User import User
from pydantic import ValidationError


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("name", "ab", "String should have at least 3 characters"),
        ("name", "a" * 51, "String should have at most 50 characters"),
        ("hashed_password", "ab", "String should have at least 3 characters"),
        ("hashed_password", "a" * 151, "String should have at most 150 characters"),
        ("email", "abc", "An email address must have an @-sign"),
        ("email", "a@.com" * 51, "value is not a valid email address"),
        ("role", "ab", "String should have at least 3 characters"),
        ("role", "a" * 21, "String should have at most 20 characters"),
    ],
)
def test_user_model(field, value, error):
    user = {"name": "test", "email": "test@gmail.com", "hashed_password": "test", "image_source": "test", "google_id": None, "role": "test"}  # noqa: SIM904

    user[field] = value

    with pytest.raises(ValidationError) as error_info:
        User(**user)

    assert error in str(error_info)
