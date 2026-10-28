def test_404_not_found(client):
    response = client.get("/non-existent-route-for-testing")
    assert response.status_code == 404
    assert b"404" in response.data
