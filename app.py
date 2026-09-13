import sqlite3
from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key"
@app.route('/', methods=['GET', 'POST'])

def index():

    return "タスク管理アプリ"

# ユーザー登録
@app.route('/register', methods=['GET', 'POST'])
def register():

    message = None

    if request.method == 'POST':

        user_name = request.form['user_name']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        with sqlite3.connect("task.db") as conn:

            cursor = conn.cursor()

            if user_name == "":
                message = "ユーザーネームが入力されていません"
                return render_template("register.html", message=message)

            elif password == "":
                message = "パスワードが入力されていません"
                return render_template("register.html", message=message)

            else:
                try:
                    cursor.execute("""
                        INSERT INTO users (name, password)
                        VALUES (?, ?)
                    """, (user_name, hashed_password))

                except sqlite3.IntegrityError:
                    message = "このユーザーネームはすでに使用されています"
                    return render_template("register.html", message=message)
                
        return redirect("/login")

    return render_template("register.html", message=message)
# ユーザーログイン
@app.route('/login', methods=['GET', 'POST'])
def login():

    message = None

    if request.method == 'POST':

        user_name = request.form['user_name']
        password = request.form['password']

        if user_name == "" or password == "":
            message = "ユーザーネームまたはパスワードが間違っています"
            return render_template("login.html", message=message)

        else:
            with sqlite3.connect("task.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, password
                    FROM users
                    WHERE name = ?
                """,(user_name,))

                user = cursor.fetchone()

                if user and check_password_hash(user[2], password):
                    session['user_id'] = user[0]
                    return redirect("/tasks")

                else:
                    message = "ユーザーネームまたはパスワードが間違っています"
                    return render_template("login.html", message=message)

    return render_template("login.html")

# タスク画面
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():

    if 'user_id' not in session:
        return redirect("/login")

    user_id = session['user_id']
    message = None

    if request.method == 'POST':

        title = request.form['task']

        if title == "":
            message = "タスクが入力されていません"

        else:
            with sqlite3.connect("task.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO tasks (user_id, title)
                    VALUES (?, ?)
                """,(user_id, title))

    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()  
        cursor.execute("""
            SELECT id, title, completed
            FROM tasks
            WHERE user_id = ?
        """,(user_id,))

        tasks = cursor.fetchall()

    return render_template("tasks.html", tasks=tasks, message=message)

# タスクを完了
@app.route('/complete/<int:task_id>')
def complete(task_id):

    if 'user_id' not in session:
        return redirect("/login")

    user_id = session['user_id']

    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET completed = 1
            WHERE id = ? AND user_id = ?
        """, (task_id, user_id))

    return redirect("/tasks")

# タスクを未完了に戻す
@app.route('/incomplete/<int:task_id>')
def incomplete(task_id):

    if 'user_id' not in session:
        return redirect("/login")

    user_id = session['user_id']

    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks
            SET completed = 0
            WHERE id = ? AND user_id = ?
        """, (task_id, user_id))

    return redirect("/tasks")

# タスクを削除
@app.route('/delete/<int:task_id>')
def delete(task_id):

    if 'user_id' not in session:
        return redirect("/login")

    user_id = session['user_id']

    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM tasks
            WHERE id = ? AND user_id = ?
        """, (task_id, user_id))

    return redirect("/tasks")

# タスク編集
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):

    if 'user_id' not in session:
        return redirect("/login")

    user_id = session['user_id']
    message = None

    with sqlite3.connect("task.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, completed
            FROM tasks
            WHERE id = ? AND user_id = ?
        """, (task_id, user_id))

        task = cursor.fetchone()

    if request.method == 'POST':

        title = request.form['edit_task']

        if title == "":
            message = "タスクが入力されていません"
            return render_template('edit.html', task=task, message=message)

        else:
            with sqlite3.connect("task.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE tasks
                    SET title = ?
                    WHERE id = ? AND user_id = ?
                """, (title, task_id, user_id))

        return redirect("/tasks")

    return render_template('edit.html', task=task, message=message)

# ログアウト
@app.route('/logout')
def logout():
    session.pop('user_id', None)

    return redirect("/login")

if __name__ == '__main__':
    app.run()