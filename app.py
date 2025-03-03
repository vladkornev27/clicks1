from flask import Flask, request, render_template, make_response
import sqlite3
import datetime
import os  # для работы с переменными окружения

app = Flask(__name__)

def log_click(role):
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clicks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT,
                    timestamp TEXT)''')
    c.execute('INSERT INTO clicks (role, timestamp) VALUES (?, ?)',
              (role, str(datetime.datetime.now())))
    conn.commit()
    conn.close()

@app.route('/phishing')
def phishing():
    role = request.args.get('role')
    if role:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('role', role)
        log_click(role)
        return resp
    else:
        return 'Роль не указана', 400

@app.route('/stats')
def stats():
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM clicks')
    clicks = c.fetchall()
    conn.close()
    return render_template('stats.html', clicks=clicks)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Используем порт из переменной окружения
    app.run(host="0.0.0.0", port=port)  # Запускаем сервер на всех интерфейсах
