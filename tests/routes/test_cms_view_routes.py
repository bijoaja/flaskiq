def test_cms_index(client):
    response = client.get("/cms", follow_redirects=True)
    assert response.status_code == 200


def test_cms_index_direct(client):
    response = client.get("/cms/")
    assert response.status_code == 200


def test_cms_page_detail_not_found(client):
    response = client.get("/cms/page/nonexistent-page")
    assert response.status_code == 404
