from flask import request, jsonify

from api import app
from models import posts_data

@app.route('/posts', methods=['POST'])
def post_posts():
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

@app.route('/posts', methods=['GET'])
def get_posts():
    # Отримуємо параметри ліміту та сторінки
    limit = request.args.get('limit', type=int, default=10)
    page = request.args.get('page', type=int, default=1)
    # Обчислюємо індекси для пагінації
    start = (page - 1) * limit
    end = start + limit
    paginated_posts = posts_data[start:end]
    response = jsonify(paginated_posts)
    # Додаємо заголовок з кількістю постів
    response.headers['post-count'] = len(posts_data)
    return response

@app.route('/posts', methods=['DELETE'])
def del_post():
    global posts_data
    data = request.get_json()['data']
    print(data)
    if 'title' not in data or 'body' not in data:
        return {'error': 'Missing title or body'}, 400
    post_id = data.get('id')
    posts_data = [post for post in posts_data if post['id'] != post_id]
    return {'message': f'Post with ID {post_id} was successfully deleted.'}, 200