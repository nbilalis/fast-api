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

###


def test_store_new_book():
    client.delete('/books/99')

    response = client.post(
        url='/books/',
        json={'id': 99, 'isbn': '1234567890', 'title': 'New Title', 'author': 'New Author', 'price': 9.99}
    )
    json = response.json()
    assert isinstance(json, dict)
    assert response.status_code == 201


def test_try_storing_new_book_with_existing_id():
    response = client.post(
        url='/books/',
        json={'id': 1, 'isbn': '1234567890', 'title': 'New Title', 'author': 'New Author', 'price': 9.99}
    )
    assert response.status_code == 409


def test_try_store_book_without_data():
    response = client.post('/books/')
    assert response.status_code == 422


def test_post_redirect():
    response = client.post('/books')
    assert response.status_code == 307
    assert response.next.path_url == '/books/'

###


def test_update_book():
    response = client.put(
        url='/books/',
        json={'id': 1, 'isbn': '111-111-1111', 'title': 'Flask', 'price': 11}
    )
    json = response.json()
    assert isinstance(json, dict)
    assert response.status_code == 200

###


def test_delete_book():
    response = client.delete('/books/99')
    assert response.status_code == 200


def test_try_deleting_non_existing_book():
    response = client.delete('/books/999')
    assert response.status_code == 404
