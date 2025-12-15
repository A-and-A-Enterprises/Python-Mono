import os
import sqlite3
import subprocess
import pickle
from flask import Flask, request

app = Flask(__name__)

# Hardcoded credentials - Critical vulnerability
DATABASE_PASSWORD = "super_secret_password_123"
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"

@app.route('/search')
def search():
    """SQL Injection vulnerability"""
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Directly interpolating user input - SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return str(results)

@app.route('/execute')
def execute_command():
    """Command Injection vulnerability"""
    filename = request.args.get('file')
    # Directly passing user input to shell command
    result = subprocess.call(f"cat {filename}", shell=True)
    return f"Command executed: {result}"

@app.route('/read')
def read_file():
    """Path Traversal vulnerability"""
    filepath = request.args.get('path')
    # No validation of file path
    with open(filepath, 'r') as f:
        content = f.read()
    return content

@app.route('/deserialize')
def deserialize_data():
    """Unsafe Deserialization vulnerability"""
    data = request.args.get('data')
    # Unsafe pickle deserialization
    obj = pickle.loads(data.encode())
    return str(obj)

@app.route('/fetch')
def fetch_url():
    """Server-Side Request Forgery (SSRF) vulnerability"""
    import requests
    url = request.args.get('url')
    # No validation of URL - SSRF
    response = requests.get(url)
    return response.text

@app.route('/eval')
def eval_code():
    """Code Injection vulnerability"""
    code = request.args.get('code')
    # Extremely dangerous - executing arbitrary code
    result = eval(code)
    return str(result)

if __name__ == '__main__':
    # Running in debug mode with hardcoded secret
    app.run(debug=True, host='0.0.0.0', port=5000)
