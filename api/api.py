from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Список користувачів
posts = [{
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  },
  {
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
  },
  {
    "userId": 1,
    "id": 3,
    "title": "ea molestias quasi exercitationem repellat qui ipsa sit aut",
    "body": "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"
  },
  {
    "userId": 1,
    "id": 9,
    "title": "eum et est occaecati",
    "body": "ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"
  }]

@app.route('/posts', methods=['GET'])
def get_users():
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    # Отримуємо дані з запиту
    data = request.get_json()

    # Перевірка на наявність необхідних полів
    if 'title' not in data or 'body' not in data:
        return jsonify({'error': 'Missing title or body'}), 400

    # Створюємо новий пост
    new_post = {
        'id': data.get('id', None),  # Якщо id не передано, можна поставити None
        'title': data['title'],
        'body': data['body']
    }

    # Додаємо пост до списку
    posts.append(new_post)

    # Відповідаємо створеним постом
    return jsonify(new_post), 201

@app.route('/posts_del', methods=['POST'])
def del_post():
    # Отримуємо дані з запиту
    global posts
    data = request.get_json()

    # Перевірка на наявність необхідних полів
    if 'title' not in data or 'body' not in data:
        return jsonify({'error': 'Missing title or body'}), 400

    # Створюємо новий пост
    new_post = {
        'id': data.get('id', None),  # Якщо id не передано, можна поставити None
        'title': data['title'],
        'body': data['body']
    }

    # Додаємо пост до списку
    posts = [post for post in posts if post['id'] != new_post["id"]]
    

    # Відповідаємо створеним постом
    return jsonify(posts), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
