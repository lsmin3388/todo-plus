import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from models import init_db, get_db, DB_PATH


@pytest.fixture
def client():
    app.config['TESTING'] = True
    test_db = DB_PATH + '.test'

    import models
    models.DB_PATH = test_db

    init_db()

    with app.test_client() as client:
        yield client

    if os.path.exists(test_db):
        os.remove(test_db)


@pytest.fixture
def sample_todo(client):
    client.post('/add', data={
        'title': 'Test Todo',
        'description': 'Test description',
        'category': 'work',
        'priority': 'high',
        'due_date': '2026-12-31'
    })


class TestIndex:
    def test_home_page_loads(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'My Todos' in response.data

    def test_empty_state(self, client):
        response = client.get('/')
        assert b'No todos found' in response.data

    def test_filter_by_category(self, client, sample_todo):
        response = client.get('/?category=work')
        assert response.status_code == 200
        assert b'Test Todo' in response.data

    def test_filter_by_priority(self, client, sample_todo):
        response = client.get('/?priority=high')
        assert response.status_code == 200
        assert b'Test Todo' in response.data

    def test_filter_by_status(self, client, sample_todo):
        response = client.get('/?status=active')
        assert response.status_code == 200
        assert b'Test Todo' in response.data


class TestCRUD:
    def test_add_page_loads(self, client):
        response = client.get('/add')
        assert response.status_code == 200
        assert b'New Todo' in response.data

    def test_create_todo(self, client):
        response = client.post('/add', data={
            'title': 'New Task',
            'description': 'Details',
            'category': 'personal',
            'priority': 'medium',
            'due_date': ''
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'New Task' in response.data

    def test_create_todo_without_title(self, client):
        response = client.post('/add', data={
            'title': '',
            'category': 'general',
            'priority': 'medium'
        }, follow_redirects=True)
        assert b'Title is required' in response.data

    def test_edit_page_loads(self, client, sample_todo):
        response = client.get('/edit/1')
        assert response.status_code == 200
        assert b'Edit Todo' in response.data

    def test_update_todo(self, client, sample_todo):
        response = client.post('/edit/1', data={
            'title': 'Updated Todo',
            'description': 'Updated desc',
            'category': 'personal',
            'priority': 'low',
            'due_date': ''
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Updated Todo' in response.data

    def test_toggle_todo(self, client, sample_todo):
        response = client.get('/toggle/1', follow_redirects=True)
        assert response.status_code == 200

    def test_delete_todo(self, client, sample_todo):
        response = client.get('/delete/1', follow_redirects=True)
        assert response.status_code == 200
        assert b'Todo deleted' in response.data

    def test_edit_nonexistent_todo(self, client):
        response = client.get('/edit/999', follow_redirects=True)
        assert b'Todo not found' in response.data


class TestStats:
    def test_stats_page_loads(self, client):
        response = client.get('/stats')
        assert response.status_code == 200
        assert b'Statistics' in response.data

    def test_stats_with_data(self, client, sample_todo):
        response = client.get('/stats')
        assert response.status_code == 200
        assert b'Total' in response.data
