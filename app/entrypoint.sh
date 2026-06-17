#!/bin/sh
# Initialise la table puis lance gunicorn (serveur WSGI de prod, pas le serveur
# de dev de Flask). On boucle tant que la base n'est pas joignable.
echo "Attente de la base PostgreSQL sur ${DB_HOST}:${DB_PORT}..."
until python -c "import psycopg2,os; psycopg2.connect(host=os.environ['DB_HOST'],port=os.environ['DB_PORT'],dbname=os.environ['DB_NAME'],user=os.environ['DB_USER'],password=os.environ['DB_PASSWORD'],connect_timeout=3)" 2>/dev/null; do
  echo "  base pas encore prête, nouvelle tentative dans 2s"
  sleep 2
done
echo "Base joignable, initialisation du schema."
python -c "import app; app.init_db()"
exec gunicorn --bind 0.0.0.0:8000 --workers 3 app:app
