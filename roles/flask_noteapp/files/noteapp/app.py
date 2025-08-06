from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'notes.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute('INSERT INTO notes (content) VALUES (?)', (note,))
        return redirect(url_for('index'))

    with sqlite3.connect(DB_PATH) as conn:
        notes = conn.execute('SELECT id, content FROM notes').fetchall()

    return render_template('index.html', notes=notes)

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
