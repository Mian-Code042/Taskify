import pytest
import json

def get_api_token(client, username, password):
    # Register first
    client.post('/register', data={'username': username, 'password': password})
    # Then get token
    response = client.post('/api/login', json={
        'username': username,
        'password': password
    })
    data = json.loads(response.data)
    return data.get('access_token')

def test_api_tasks_crud(client, app):
    """Test full API CRUD lifecycle"""
    token = get_api_token(client, 'apiuser', 'StrongPassword123')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 1. POST Task
    post_res = client.post('/api/tasks', headers=headers, json={
        'title': 'API Task',
        'priority': 'Low'
    })
    assert post_res.status_code == 201
    post_data = json.loads(post_res.data)
    task_id = post_data['task']['id']
    
    # 2. GET Tasks
    get_res = client.get('/api/tasks', headers=headers)
    assert get_res.status_code == 200
    assert b"API Task" in get_res.data
    
    # 3. PUT (Update) Task
    put_res = client.put(f'/api/tasks/{task_id}', headers=headers, json={
        'status': 'Completed'
    })
    assert put_res.status_code == 200
    put_data = json.loads(put_res.data)
    assert put_data['task']['status'] == 'Completed'
    assert put_data['task']['complete'] == True
    
    # 4. DELETE Task
    del_res = client.delete(f'/api/tasks/{task_id}', headers=headers)
    assert del_res.status_code == 200
    assert b"Task deleted" in del_res.data
    
    # Verify deletion
    final_get = client.get('/api/tasks', headers=headers)
    assert b"API Task" not in final_get.data
