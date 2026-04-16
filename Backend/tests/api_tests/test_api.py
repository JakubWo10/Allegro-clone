def create_headers():
    headers = {"Authorization": "Bearer fake-token"}
    return headers


def test_get_my_profile(authorized_client):

    headers = create_headers()
    response = authorized_client.get("/me", headers=headers)

    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "test"
    assert data["image_source"] == "test"


def test_get_my_profile_without_token(unauthorized):
    headers = create_headers()

    response = unauthorized.get("/me", headers=headers)

    assert response.status_code == 401
