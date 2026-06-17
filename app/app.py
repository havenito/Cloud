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
    body {
      font-family: ui-monospace, "DejaVu Sans Mono", monospace;
      background: #f6f6f3;
      color: #1c1c1c;
      margin: 0;
      padding: 70px 20px;
    }
    .box {
      max-width: 460px;
      margin: 0 auto;
      background: #fff;
      border: 1px solid #d8d8d3;
      padding: 26px 30px;
    }
    .status {
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 12.5px;
      color: #2f6f4f;
      margin-bottom: 18px;
    }
    .dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #2f6f4f;
    }
    h1 {
      font-size: 15.5px;
      font-weight: 600;
      margin: 0 0 18px;
      color: #1c1c1c;
    }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    td { padding: 7px 0; border-bottom: 1px solid #eee; }
    td.k { color: #888; width: 45%; }
    .count { font-weight: 700; }
  </style>
</head>
<body>
  <div class="box">
    <div class="status"><span class="dot"></span>service en ligne</div>
    <h1>app-flask // demo cloud computing</h1>
    <table>
      <tr><td class="k">visites enregistrees</td><td class="count">{{ count }}</td></tr>
      <tr><td class="k">conteneur</td><td>{{ host }}</td></tr>
      <tr><td class="k">base de donnees</td><td>postgresql @ {{ db_host }}</td></tr>
    </table>
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