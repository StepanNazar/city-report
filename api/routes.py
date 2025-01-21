from flask import request

from api import app
from models import posts_data

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        return posts_data
    data = request.get_json()
    if 'title' not in data or 'body' not in data:
        return {'error': 'Missing title or body'}, 400
    new_post = {
        'id': data.get('id'),
        'title': data['title'],
        'body': data['body']
    }
    posts_data.append(new_post)
    return new_post, 201

@app.route('/posts_del', methods=['POST'])
def del_post():
    global posts_data
    data = request.get_json()
    if 'title' not in data or 'body' not in data:
        return {'error': 'Missing title or body'}, 400
    post_id = data.get('id')
    posts_data = [post for post in posts_data if post['id'] != post_id]
    return posts_data, 201