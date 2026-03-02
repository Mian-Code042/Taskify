import pytest
from app.models import User, Todo, db

def test_user_registration(client, app):
    """Test successful user registration with valid password"""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'StrongPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Registration successful" in response.data
    
    with app.app_context():
        user = User.query.filter_by(username='newuser').first()
        assert user is not None

def test_user_login(client, app):
    """Test login functionality"""
    # First register a user
    client.post('/register', data={
        'username': 'loginuser',
        'password': 'StrongPassword123'
    })
    
    # Then try to login
    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'StrongPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data
    assert b"Logout" in response.data

def test_task_creation(client, app):
    """Test that a logged in user can create a task"""
    # Setup - Register and Login
    client.post('/register', data={'username': 'taskuser', 'password': 'StrongPassword123'})
    client.post('/login', data={'username': 'taskuser', 'password': 'StrongPassword123'})
    
    # Create Task
    response = client.post('/add', data={
        'title': 'My new test task',
        'priority': 'High'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Task added!" in response.data
    assert b"My new test task" in response.data

def test_task_isolation(client, app):
    """Test that user1 cannot see or delete user2's tasks"""
    # User 1 registers, logs in, adds task
    client.post('/register', data={'username': 'user1', 'password': 'StrongPassword123'})
    client.post('/login', data={'username': 'user1', 'password': 'StrongPassword123'})
    client.post('/add', data={'title': 'User 1 Task'})
    client.get('/logout')
    
    # User 2 registers, logs in, adds task
    client.post('/register', data={'username': 'user2', 'password': 'StrongPassword123'})
    client.post('/login', data={'username': 'user2', 'password': 'StrongPassword123'})
    client.post('/add', data={'title': 'User 2 Task'})
    
    # Verify User 2 sees their own task, but not User 1's
    response = client.get('/', follow_redirects=True)
    assert b"User 2 Task" in response.data
    assert b"User 1 Task" not in response.data
    
    # Try to delete User 1's task directly
    with app.app_context():
        user1_task = Todo.query.filter_by(title='User 1 Task').first()
        task_id = user1_task.id
        
    response = client.post(f'/delete/{task_id}', follow_redirects=True)
    assert b"Unauthorized to delete this task" in response.data
