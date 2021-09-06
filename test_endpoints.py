# Testing Python in Visual Studio Code - https://tmpl.at/2YmG9CY

from main import app

from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_books():
    response = client.get('/books/')
    json = response.json()
    assert isinstance(json, list)
    assert response.status_code == 200


def test_get_book_by_id():
    response = client.get('/books/1')
    json = response.json()
    assert isinstance(json, dict)
    assert response.status_code == 200


def test_get_non_existing_book():
    response = client.get('/books/999')
    assert response.status_code == 404


def test_store_book_none():
    response = client.post('/books/')
    assert response.status_code == 422


def test_post_redirect():
    response = client.post('/books')
    assert response.status_code == 307
    assert response.next.path_url == '/books/'
