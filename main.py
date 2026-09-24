from flask import render_template, g, request
import sqlite3

DATABASE = 'database.db' # Remplacez par le nom de votre base de données si besoin

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialiser la table des statistiques au démarrage
def init_counter():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS site_stats (
                id INTEGER PRIMARY KEY,
                total_views INTEGER NOT NULL
            )
        ''')
        # S'assurer qu'une ligne de compteur existe
        cursor.execute('SELECT COUNT(*) FROM site_stats')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO site_stats (id, total_views) VALUES (1, 0)')
        db.commit()

# Appeler cette fonction au lancement de l'app (avant d'exécuter app.run)
# init_counter()

# Incrémenter le compteur à chaque visite de page (sauf fichiers statiques CSS/JS)
@app.before_request
def count_visitor():
    if request.endpoint == 'static':
        return
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE site_stats SET total_views = total_views + 1 WHERE id = 1')
    db.commit()

# Exemple de route pour passer le nombre de vues à votre template HTML
@app.route('/')
def home():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT total_views FROM site_stats WHERE id = 1')
    row = cursor.fetchone()
    views = row[0] if row else 0
    
    return render_template('index.html', views=views)
