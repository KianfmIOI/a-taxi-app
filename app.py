from flask import Flask, request, jsonify
from json import load, dump

app = Flask(__name__)
JSON_FILE = 'users.json'


def read_users():
    try:
        with open(JSON_FILE, 'r') as file:
            return load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print("Error reading file:", e)
        return {}


def write_users(data):
    try:
        with open(JSON_FILE, 'w') as file:
            dump(data, file, indent=4)
    except Exception as e:
        print("Error writing file:", e)


@app.route('/users', methods=['GET'])
def get_users():
    users = read_users()
    return jsonify(users)


@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json  # Expecting JSON data in request body
    users = read_users()
    username = new_user.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    users[username] = new_user
    write_users(users)
    return jsonify({'message': 'User added successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True, port=8000)
