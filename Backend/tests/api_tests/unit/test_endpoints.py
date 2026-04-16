from unittest.mock import AsyncMock, MagicMock

import pytest
from api.api import get_my_data, login, register
from api.api_models.RegUser import Reguser
from api.exceptions import MyHttpException
from fastapi import HTTPException


def user_db_return_value():
    return {"user_id": 1, "hashed_password": "123", "name": "Jacek", "email": "jacek@test.pl", "image_source": "test", "role": "user"}


@pytest.mark.asyncio
async def test_get_me() -> None:

    fake_user_data = {"user_id": 1, "name": "Jacek", "email": "jacek@test.pl", "role": "admin"}
    res = await get_my_data(user=fake_user_data)
    assert res["name"] == "Jacek"


@pytest.mark.asyncio
async def test_register_correct_data() -> None:
    fake_user_data = {"name": "Jacek", "email": "jacek@test.pl", "password": "Super-secret-password"}

    mock_service = AsyncMock()
    mock_service.user_name_exist.return_value = False
    mock_service.insert_user.return_value = True

    reg_data = Reguser(**fake_user_data)

    result = await register(reg_user=reg_data, service=mock_service)

    assert result["detail"] == "Sucessful register"


@pytest.mark.asyncio
async def test_register_incorrect_data() -> None:
    fake_user_data = {"name": "Dwa", "email": "jacek@test.pl", "password": "Super-secret-password"}

    status_code = 409
    mock_service = AsyncMock()
    mock_service._user_name_exist.return_value = True

    reg_user = Reguser(**fake_user_data)

    with pytest.raises(HTTPException) as error_info:
        await register(reg_user=reg_user, service=mock_service)

    assert MyHttpException.NAME_IS_TAKEN in error_info.value.detail
    assert status_code == error_info.value.status_code


@pytest.mark.asyncio
async def test_login_correct_data() -> None:

    user = MagicMock()
    user.username = "Jacek"
    user.password = "Jackson"

    mock_service = AsyncMock()
    mock_service.user_exist_all_data.return_value = {"user_id": 1, "hashed_password": "123", "name": "Jacek", "email": "jacek@test.pl", "image_source": "test", "role": "user"}
    verify_password = MagicMock()
    verify_password.return_value = True

    result = await login(form_data=user, service=mock_service, verify=verify_password)

    assert result["username"] == "Jacek"
    assert result["user_email"] == "jacek@test.pl"


@pytest.mark.asyncio
async def test_login_user_doesnt_exist() -> None:

    user = MagicMock()
    user.username = "Jacek"
    user.password = "Jackowski"

    mock_service = AsyncMock()
    mock_service.user_exist_all_data.return_value = False

    verfiy = MagicMock()
    verfiy.return_value = False
    status_code = 401

    with pytest.raises(HTTPException) as error_info:
        await login(form_data=user, service=mock_service, verify=verfiy)

    assert MyHttpException.UNAUTHORIZED == error_info.value.detail
    assert status_code == error_info.value.status_code


@pytest.mark.asyncio
async def test_login_user_incorrect_password() -> None:

    user = MagicMock()
    user.username = "Jacek"
    user.password = "Jackowski"

    mock_service = AsyncMock()
    mock_service.user_exist_all_data.return_value = True

    verfiy = MagicMock()
    verfiy.return_value = False

    status_code = 401

    with pytest.raises(HTTPException) as error_info:
        await login(form_data=user, service=mock_service, verify=verfiy)

    assert status_code == error_info.value.status_code
    assert MyHttpException.INVALID_PASSWORD == error_info.value.detail
