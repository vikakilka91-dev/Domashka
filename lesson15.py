import pymysql
from flask import Flask, request, render_template_string, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-me-super-secret-key" # Обязательно для работы session и flash

# ==========================================
# КЛАСС DATABASE (Имитация database.py)
# ==========================================
class Database:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        # ВНИМАНИЕ: Замените 'your_password' на ваш пароль от MySQL!
        self.password = 'your_password' 
        self.db_name = 'flask_auth'

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    # Пункт 3: Метод БД create_user
    def create_user(self, name, password):
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (user_name, user_password) VALUES (%s, %s)"
                cursor.execute(sql, (name, password))
                connection.commit() # Фиксируем изменения
                return cursor.lastrowid # Возвращаем ID нового пользователя
        finally:
            connection.close()

db = Database()

# ==========================================
# HTML ШАБЛОНЫ (Имитация папки templates)
# ==========================================
# Базовые стили для красивого вывода
STYLES = """
<style>
    body { font-family: Arial, sans-serif; background: #1e1e2e; color: #cdd6f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .box { background: #313244; padding: 30px; border-radius: 10px; width: 350px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    h2 { text-align: center; }
    input { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; border-radius: 5px; border: 1px solid #45475a; background: #1e1e2e; color: white; }
    button { width: 100%; padding: 10px; background: #89b4fa; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; color: #11111b; }
    button:hover { background: #b4befe; }
    .error { background: #f38ba8; color: #11111b; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px; }
    .success { background: #a6e3a1; color: #11111b; padding: 10px; border-radius: 5px; text-align: center; }
    a { color: #89b4fa; text-decoration: none; display: block; text-align: center; margin-top: 15px; }
</style>
"""

REGISTER_HTML = STYLES + """
<div class="box">
    <h2>Регистрация</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="error">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}
    <form method="POST" action="/register">
        <input type="text" name="username" placeholder="Имя" required>
        <input type="password" name="password" placeholder="Пароль" required>
        <button type="submit">Зарегистрироваться</button>
    </form>
    <a href="/login">Уже есть аккаунт? Войти</a>
</div>
"""

PROFILE_HTML = STYLES + """
<div class="box">
    <h2>Профиль</h2>
    <div class="success">Добро пожаловать, {{ username }}!</div>
    <a href="/login">Выйти</a>
</div>
"""

# ==========================================
# МАРШРУТЫ (ROUTES)
# ==========================================
# Для теста перенаправим корень на регистрацию
@app.route('/')
def index():
    return redirect(url_for('register'))

# Пункт 1 и 2: GET и POST для /register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Пункт 2: Принять request.form, проверить на пустоту
        name = request.form.get("username", "").strip()
        pwd = request.form.get("password", "").strip()

        if not name or not pwd:
            flash("Заполните все поля!")
            return render_template_string(REGISTER_HTML)

        try:
            # Вызов метода БД (Пункт 3)
            user_id = db.create_user(name, pwd)
            
            # Пункт 4: Успех -> session -> profile.html
            session['user_id'] = user_id
            session['username'] = name
            return redirect(url_for('profile'))
            
        except pymysql.err.IntegrityError:
            # Пункт 5: Ошибка (дубль имени) -> register.html с текстом ошибки
            flash("Пользователь с таким именем уже существует.")
            return render_template_string(REGISTER_HTML)
        except Exception as e:
            # Обработка других ошибок БД
            flash(f"Ошибка БД: {e}")
            return render_template_string(REGISTER_HTML)

    # GET запрос: просто отдаем форму (Пункт 1)
    return render_template_string(REGISTER_HTML)

@app.route("/profile")
def profile():
    # Защита страницы профиля: если нет сессии, кидаем на регистрацию
    if 'username' not in session:
        return redirect(url_for('register'))
    
    # Отдаем профиль с приветствием
    return render_template_string(PROFILE_HTML, username=session['username'])

if __name__ == "__main__":
    app.run(debug=True)
