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
        INSERT INTO commits (filename, code, message, created_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (data['filename'], data['code'], data['message'], datetime.now()))
    
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
