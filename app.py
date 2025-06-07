from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

USERS_FILE = 'users.json'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def style():
    return send_from_directory('.', 'styles.css')

@app.route('/users', methods=['GET'])
def get_users():
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    # Check if username already exists
    if any(user['username'] == new_user['username'] for user in users):
        return jsonify({'error': 'Username already exists'}), 400

    users.append(new_user)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    return jsonify({'message': 'User added successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    username = credentials.get('username')
    password = credentials.get('password')

    with open(USERS_FILE, 'r') as f:
        users = json.load(f)

    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({'message': 'Login successful!'}), 200

    return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(port=8000)
