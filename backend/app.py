from flask import Flask, jsonify
from flask_cors import CORS
import os, time
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_NAME = os.getenv('POSTGRES_DB', 'mydb')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'postgres')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')

def get_conn(retries=10, delay=1):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
            )
            return conn
        except Exception as e:
            print(f"Intento {i+1}/{retries} - DB no lista: {e}")
            time.sleep(delay)
    raise Exception("No se pudo conectar a la base de datos")

@app.route('/')
def root():
    return jsonify(message="Backend OK")

@app.route('/message')
def message():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT id, text FROM notes;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # concatenamos textos de la tabla
    texts = [r['text'] for r in rows]
    return jsonify(message=" | ".join(texts) if texts else "Sin notas en DB")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
