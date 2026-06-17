import os
import socket
import psycopg2
from flask import Flask, render_template_string
 
app = Flask(__name__)
 
# infos de connexion à la base (definies dans compose.yml)
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "techapp")
DB_USER = os.environ.get("DB_USER", "techapp")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "changeme")
 
 
def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD, connect_timeout=5
    )
 
 
def init_db():
    # cree la table si elle existe pas encore
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visites (id SERIAL PRIMARY KEY, vu_le TIMESTAMP DEFAULT NOW());")
    conn.commit()
    cur.close()
    conn.close()
 
 
PAGE = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Demo Cloud Computing</title>
  <style>
    body { font-family: system-ui, sans-serif; background:#1b1230; color:#eee;
           display:flex; align-items:center; justify-content:center; height:100vh; margin:0; }
    .card { background:#2a1d4a; padding:2.5rem 3rem; border-radius:14px;
            box-shadow:0 10px 40px rgba(0,0,0,.4); text-align:center; }
    h1 { margin-top:0; color:#b794f6; }
    .count { font-size:3rem; font-weight:700; color:#fff; }
    .meta { color:#9d8ec2; font-size:.9rem; margin-top:1rem; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Application web conteneurisée</h1>
    <p>Nombre de visites enregistrées en base :</p>
    <div class="count">{{ count }}</div>
    <p class="meta">Servie par le conteneur applicatif : <b>{{ host }}</b><br>
       Base de données : PostgreSQL sur {{ db_host }}</p>
  </div>
</body>
</html>
"""
 
 
@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visites DEFAULT VALUES;")
    cur.execute("SELECT COUNT(*) FROM visites;")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return render_template_string(PAGE, count=count, host=socket.gethostname(), db_host=DB_HOST)
 
 
@app.route("/health")
def health():
    # utilisé par le reverse proxy pour checker que l'app repond
    try:
        conn = get_connection()
        conn.close()
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "ko", "error": str(e)}, 503
 
 
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)