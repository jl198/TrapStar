from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/add_two_nums', methods=['POST'])
def add_two_nums():
    # get two nums from post
    data_dict = request.get_json()
    x, y = data_dict["x"], data_dict["y"]
    z = x + y
    # return JSON with both nums and their sum
    return_JSON = {
        "z": z
    }
    return jsonify(return_JSON), 200

@app.route('/hithere')
def hi_there_everyone():
    return "I just hit /hithere"

if __name__ == '__main__':
    app.run(debug=True)
