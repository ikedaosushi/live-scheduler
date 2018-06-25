from flask import Flask , jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/')
def index():
    res = {
        'status_code': 200,
        'text': 'This is live scheduler'
    }

    return jsonify(res)

@app.route('/api/random', methods=['GET'])
def random_number():
    res = {
        'status_code': 200,
        'randomNumber': randint(1, 100)
    }

    return jsonify(res)


if __name__ == '__main__':
    app.run()