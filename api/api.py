from flask import Flask

app = Flask(__name__)

import routes, models

if __name__ == '__main__':
    app.run(debug=True, port=5000)
