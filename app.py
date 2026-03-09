from flask import Flask, g, render_template
import sqlite3

DATABASE = 'boynextdoordb.db'

#initialising app
app = Flask(__name__)


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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def home():
    sql = "SELECT * FROM Album;"
    albums = query_db(sql)
    return render_template("home.html", albums=albums)

@app.route("/songs/<int:id>")
def songs(id):
    sql = """
        SELECT * FROM songs
        WHERE albumID = ?
        ORDER BY songID;
    """
    songs = query_db(sql, [id])

    album_sql = "SELECT * FROM Album WHERE albumID = ?"
    album = query_db(album_sql, [id], one=True)

    return render_template("songs.html", songs=songs, album=album)

if __name__ == "__main__":
    app.run(debug=True)