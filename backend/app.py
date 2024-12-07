from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="codedb",
        user="postgres",
        password="password"
    )

@app.route('/commit', methods=['POST'])
def create_commit():
    data = request.json
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO commits (filename, code, message, created_at, username)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (data['filename'], data['code'], data['message'], 
          datetime.now(), data['username']))
    
    commit_id = cur.fetchone()[0]
    conn.commit()
    
    cur.close()
    conn.close()
    
    return jsonify({'id': commit_id}), 201


@app.route('/commits', methods=['GET'])
def get_commits():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT * FROM commits ORDER BY created_at DESC")
    commits = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return jsonify(commits)

@app.route('/commit/<int:commit_id>', methods=['DELETE'])
def delete_commit(commit_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM commits WHERE id = %s", (commit_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    return jsonify({'status': 'deleted'}), 204

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                (username, password))
    user = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if user:
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Создание таблицы users (только если её нет)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password VARCHAR(120) NOT NULL
        )
    """)

    # Создание таблицы commits (только если её нет)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS commits (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            code TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            username VARCHAR(80) NOT NULL
        )
    """)
    
    # Проверка существования пользователей
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    
    # Добавление тестовых пользователей, только если их нет
    if count == 0:
        cur.execute("""
            INSERT INTO users (username, password) VALUES
            ('user1', '111'),
            ('user2', '222')
        """)
    
    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)