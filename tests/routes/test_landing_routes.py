def test_landing_index(client):
    response = client.get("/")
    assert response.status_code == 200
