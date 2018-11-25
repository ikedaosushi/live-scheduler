from flask import Flask , jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSON_AS_ASCII'] = False 

from dotenv import load_dotenv
import os
from pathlib import Path

pj_dir = Path(__file__).parents[1]

load_dotenv(pj_dir/'.env')

from boto3.session import Session

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
aws_secret_access_key = os.environ.get('AWS_SECRET_KEY')

session = Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
dynamodb = session.resource('dynamodb', region_name='ap-northeast-1')

@app.route('/')
def index():
    res = {
        'status_code': 200,
        'text': "welcome live scheduler" 
    }

    return jsonify(res)

@app.route('/events')
def lives():
    table_name = 'live-scheduler'
    table = dynamodb.Table(table_name)
    lives = table.scan()['Items']

    res = {
        'status_code': 200,
        'events': lives
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