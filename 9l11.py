from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages' # Нужен для работы flash-сообщений

# Имитация базы данных (словарь)
USERS_DB = {
    "admin": "12345",
    "student": "qwerty"
}

# Встроенный HTML-шаблон (вместо папки templates)
# В реальном проекте этот код выносится в отдельный файл templates/index.html
INDEX_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Авторизация</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #1e1e2e; color: #cdd6f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background-color: #313244; padding: 30px; border-radius: 10px; width: 350px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h2 { text-align: center; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-size: 14px; color: #a6adc8; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; box-sizing: border-box; border-radius: 5px; border: 1px solid #45475a; background-color: #1e1e2e; color: white; }
        input:focus { outline: none; border-color: #89b4fa; }
        button { width: 100%; padding: 10px; background-color: #89b4fa; color: #11111b; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background-color: #b4befe; }
        .error { background-color: #f38ba8; color: #11111b; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 14px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Вход в систему</h2>
        
        <!-- Блок вывода ошибки -->
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="error">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <!-- Форма (Пункт 2) -->
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">ИМЯ ПОЛЬЗОВАТЕЛЯ</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">ПАРОЛЬ</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Войти</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Если пользователь зашел на главную, перенаправляем на страницу логина
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    # Отдаем HTML шаблон (Пункт 4)
    return render_template_string(INDEX_HTML)

@app.route('/login', methods=['POST'])
def login():
    # Получаем данные из формы (request.form)
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        # Проверка на пустые поля (Пункт 3)
        if not username or not password:
            raise ValueError("Поля не могут быть пустыми")

        # Проверка логина и пароля по словарю (Пункт 1)
        if username in USERS_DB and USERS_DB[username] == password:
            # Успешный вход: перенаправление (Пункт 4)
            # В реальном приложении здесь был бы переход на дашборд
            return "Успешный вход! Добро пожаловать."
        else:
            # Неверные данные: вызываем исключение
            raise ValueError("Неверное имя пользователя или пароль")

    except ValueError as e:
        # Обработка ошибки (Пункт 5)
        # Передаем сообщение об ошибке через flash
        flash(str(e))
        # Остаемся на странице логина
        return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
