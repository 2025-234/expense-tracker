from flask import Flask, render_template, g, request
import sqlite3

# 1. INITIALISATION DE FLASK EN PREMIER
app = Flask(__name__)

DATABASE = 'expenses.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

# 2. FERMETURE DE LA CONNEXION (Utilise @app, donc placé après la création de app)
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 3. FONCTION POUR GÉRER LE COMPTEUR DE VISITES
def get_visitor_count():
    db = get_db()
    cursor = db.cursor()
    # Création d'une table stats si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visits INTEGER
        )
    ''')
    cursor.execute('SELECT visits FROM stats WHERE id = 1')
    row = cursor.fetchone()
    
    if row is None:
        cursor.execute('INSERT INTO stats (id, visits) VALUES (1, 1)')
        db.commit()
        return 1
    else:
        new_visits = row['visits'] + 1
        cursor.execute('UPDATE stats SET visits = ? WHERE id = 1', (new_visits,))
        db.commit()
        return new_visits

# 4. ROUTE PRINCIPALE
@app.route('/')
def index():
    count = get_visitor_count()
    # Vous pouvez rajouter ici la récupération de vos dépenses si besoin
    return render_template('index.html', count=count)

# 5. LANCEMENT LOCAL (ignoré par Render qui utilise Gunicorn)
if __name__ == '__main__':
    app.run(debug=True)
