import bcrypt
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db['Users']


class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username, password = posted_data['username'], posted_data['password']
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_password,
            "Sentence": "",
            "Tokens": 5
        })

        return_json = {
            'status': 200,
            'message': 'You successfully signed up for the API'
        }
        return jsonify(return_json)


def verify_password(username, password):
    hashed_password = users.find({
        "Username": username
    })[0]["Password"]
    return bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password


def get_tokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


class Store(Resource):
    def post(self):
        posted_data = request.get_json()
        username, password = posted_data['username'], posted_data['password']
        sentence = posted_data['sentence']
        password_is_correct = verify_password(username, password)
        if password_is_correct is False:
            return_json = {
                'status': 302
            }
            return jsonify(return_json)
        user_tokens = get_tokens(username)
        if user_tokens <= 0:
            return_json = {
                'status': 301
            }
            return jsonify(return_json)

        users.update({
            "Username": username
        }, {
            "$set": {"Sentence": sentence,
                     "Tokens": user_tokens - 1
                     }
        })

        return_json = {
            'status': 200,
            'message': 'Sentence saved successfully!'
        }


class Get(Resource):
    def post(self):
        posted_data = request.get_json()
        username, password = posted_data['username'], posted_data['password']
        password_is_correct = verify_password(username, password)

        if password_is_correct is False:
            return_json = {
                'status': 302
            }
            return jsonify(return_json)
        user_tokens = get_tokens(username)
        if user_tokens <= 0:
            return_json = {
                'status': 301
            }
            return jsonify(return_json)

        users.update({
            "Username": username
        }, {
            "$set": {
                "Tokens": user_tokens - 1
            }
        })

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        return_json = {
            'status': 200,
            'sentence': str(sentence)
        }
        return jsonify(return_json)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


@app.route('/')
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
