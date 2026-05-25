# ============================================================
# app.py - VERSÃO SEGURA (CORRIGIDA)
# ✅ Usa prepared statements para prevenir SQL Injection
# ============================================================

import re
from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash)
from db_config import get_connection

app = Flask(__name__)
app.secret_key = "chave_segura_com_entropia_suficiente_XkP9#mQ2"


# ============================================================
# HELPERS DE VALIDAÇÃO
# ============================================================

def is_valid_username(username: str) -> bool:
    """Permite apenas letras, números e underscore (3–30 chars)."""
    return bool(re.fullmatch(r"[a-zA-Z0-9_]{3,30}", username))


def is_valid_year(year: str) -> bool:
    """Verifica se o ano está em um intervalo razoável."""
    try:
        y = int(year)
        return 1800 <= y <= 2099
    except (ValueError, TypeError):
        return False


def is_valid_quantity(qty: str) -> bool:
    try:
        return int(qty) >= 0
    except (ValueError, TypeError):
        return False


# ============================================================
# ROTA RAIZ → redireciona para login
# ============================================================
@app.route("/")
def index():
    return redirect(url_for("login"))


# ============================================================
# LOGIN - ✅ SEGURO: prepared statement
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Validação básica de entrada
        if not username or not password:
            flash("Preencha todos os campos.", "warning")
            return render_template("login.html")

        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ✅ PREPARED STATEMENT: parâmetros passados separadamente,
        #    nunca concatenados na string SQL.
        query = "SELECT * FROM users WHERE username=%s AND password=%s"

        print("\n" + "="*60)
        print("✅ [SEGURO] Query de login (prepared statement):")
        print(f"    {query}")
        print(f"    Parâmetros: ({username!r}, ***)")
        print("="*60 + "\n")

        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session["user_id"]  = user["id"]
            session["username"] = user["username"]
            session["role"]     = user["role"]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuário ou senha inválidos!", "danger")

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================
@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))


# ============================================================
# DASHBOARD
# ============================================================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM books")
    total_books = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM users")
    total_users = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return render_template("dashboard.html",
                           total_books=total_books,
                           total_users=total_users)


# ============================================================
# LISTAR LIVROS + BUSCA - ✅ SEGURO: prepared statement
# ============================================================
@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        # ✅ PREPARED STATEMENT: o valor de `search` nunca é
        #    inserido diretamente na string SQL.
        query  = "SELECT * FROM books WHERE title LIKE %s ORDER BY title"
        param  = f"%{search}%"

        print("\n" + "="*60)
        print("✅ [SEGURO] Query de busca (prepared statement):")
        print(f"    {query}")
        print(f"    Parâmetros: ({param!r},)")
        print("="*60 + "\n")

        cursor.execute(query, (param,))
    else:
        cursor.execute("SELECT * FROM books ORDER BY title")

    book_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("books.html", books=book_list, search=search)


# ============================================================
# ADICIONAR LIVRO (somente admin)
# ============================================================
@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Acesso negado. Somente administradores.", "danger")
        return redirect(url_for("books"))

    if request.method == "POST":
        title        = request.form.get("title", "").strip()
        author       = request.form.get("author", "").strip()
        category     = request.form.get("category", "").strip()
        publish_year = request.form.get("publish_year", "").strip()
        quantity     = request.form.get("quantity", "1").strip()

        # ✅ Validação de campos obrigatórios
        if not all([title, author, category, publish_year, quantity]):
            flash("Todos os campos são obrigatórios.", "warning")
            return render_template("add_book.html")

        if not is_valid_year(publish_year):
            flash("Ano de publicação inválido (1800–2099).", "warning")
            return render_template("add_book.html")

        if not is_valid_quantity(quantity):
            flash("Quantidade deve ser um número inteiro ≥ 0.", "warning")
            return render_template("add_book.html")

        conn   = get_connection()
        cursor = conn.cursor()

        # ✅ PREPARED STATEMENT
        cursor.execute(
            "INSERT INTO books (title, author, category, publish_year, quantity) "
            "VALUES (%s, %s, %s, %s, %s)",
            (title, author, category, int(publish_year), int(quantity))
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Livro adicionado com sucesso!", "success")
        return redirect(url_for("books"))

    return render_template("add_book.html")


# ============================================================
# EDITAR LIVRO (somente admin)
# ============================================================
@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Acesso negado. Somente administradores.", "danger")
        return redirect(url_for("books"))

    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        title        = request.form.get("title", "").strip()
        author       = request.form.get("author", "").strip()
        category     = request.form.get("category", "").strip()
        publish_year = request.form.get("publish_year", "").strip()
        quantity     = request.form.get("quantity", "1").strip()

        if not all([title, author, category, publish_year, quantity]):
            flash("Todos os campos são obrigatórios.", "warning")
            cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
            book = cursor.fetchone()
            return render_template("edit_book.html", book=book)

        if not is_valid_year(publish_year):
            flash("Ano de publicação inválido.", "warning")
            cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
            book = cursor.fetchone()
            return render_template("edit_book.html", book=book)

        if not is_valid_quantity(quantity):
            flash("Quantidade inválida.", "warning")
            cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
            book = cursor.fetchone()
            return render_template("edit_book.html", book=book)

        # ✅ PREPARED STATEMENT
        cursor.execute(
            "UPDATE books SET title=%s, author=%s, category=%s, "
            "publish_year=%s, quantity=%s WHERE id=%s",
            (title, author, category, int(publish_year), int(quantity), book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for("books"))

    # ✅ PREPARED STATEMENT
    cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()

    if not book:
        flash("Livro não encontrado.", "danger")
        return redirect(url_for("books"))

    return render_template("edit_book.html", book=book)


# ============================================================
# DELETAR LIVRO (somente admin)
# ============================================================
@app.route("/books/delete/<int:book_id>")
def delete_book(book_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Acesso negado. Somente administradores.", "danger")
        return redirect(url_for("books"))

    conn   = get_connection()
    cursor = conn.cursor()
    # ✅ PREPARED STATEMENT
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Livro removido com sucesso!", "success")
    return redirect(url_for("books"))


# ============================================================
# INICIAR APLICAÇÃO
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("✅ Rodando versão SEGURA (prepared statements)")
    print("   Porta: 5001")
    print("="*60 + "\n")
    app.run(debug=True, port=5001)
