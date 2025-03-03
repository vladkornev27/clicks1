from flask import Flask, request, render_template, make_response
import sqlite3
import datetime

app = Flask(__name__)

def log_click(role):
    # Подключаемся к базе данных
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()

    # Создаем таблицу, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS clicks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT,
                    timestamp TEXT)''')

    # Вставляем новую запись с ролью и временем клика
    c.execute('INSERT INTO clicks (role, timestamp) VALUES (?, ?)',
              (role, str(datetime.datetime.now())))

    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение



# Маршрут для фиксации кликов
@app.route('/phishing')
def phishing():
    role = request.args.get('role')  # Получаем роль пользователя из параметров
    if role:
        # Сохраняем роль в куки
        resp = make_response(render_template('index.html'))
        resp.set_cookie('role', role)
        log_click(role)  # Логируем клик в базе данных
        return resp
    else:
        return 'Роль не указана', 400

# Маршрут для отображения статистики кликов
@app.route('/stats')
def stats():
    conn = sqlite3.connect('clicks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM clicks')  # Получаем все данные из таблицы
    clicks = c.fetchall()
    conn.close()
    return render_template('stats.html', clicks=clicks)  # Передаем данные на страницу

if __name__ == '__main__':
    app.run(debug=True)
