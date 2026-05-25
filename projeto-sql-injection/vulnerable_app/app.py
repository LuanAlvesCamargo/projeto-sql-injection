# ============================================================
# app.py - VERSÃO VULNERÁVEL A SQL INJECTION
# ⚠️  ATENÇÃO: Este código é PROPOSITALMENTE inseguro!
#     Fins didáticos apenas. NÃO use em produção!
# ============================================================

from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash)
from db_config import get_connection

app = Flask(__name__)
app.secret_key = "chave_super_secreta_vulneravel_123"


# ============================================================
# ROTA RAIZ → redireciona para login
# ============================================================
@app.route("/")
def index():
    return redirect(url_for("login"))


# ============================================================
# LOGIN - ⚠️ VULNERÁVEL A SQL INJECTION
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ⚠️ SQL INJECTION: string concatenation direta!
        # Exemplo de ataque: username = ' OR '1'='1
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        # Imprime a query no terminal para fins didáticos
        print("\n" + "="*60)
        print("⚠️  [VULNERÁVEL] Query de login executada:")
        print(f"    {query}")
        print("="*60 + "\n")

        cursor.execute(query)
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
# LISTAR LIVROS + BUSCA - ⚠️ VULNERÁVEL A SQL INJECTION
# ============================================================
@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "")
    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        # ⚠️ SQL INJECTION: entrada do usuário direto na query!
        query = f"SELECT * FROM books WHERE title LIKE '%{search}%' ORDER BY title"

        print("\n" + "="*60)
        print("⚠️  [VULNERÁVEL] Query de busca executada:")
        print(f"    {query}")
        print("="*60 + "\n")
    else:
        query = "SELECT * FROM books ORDER BY title"

    cursor.execute(query)
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
        title        = request.form.get("title", "")
        author       = request.form.get("author", "")
        category     = request.form.get("category", "")
        publish_year = request.form.get("publish_year", "")
        quantity     = request.form.get("quantity", 1)

        conn   = get_connection()
        cursor = conn.cursor()

        # INSERT usa %s aqui apenas por ser menos visado na demo,
        # mas o foco da vulnerabilidade está no login e busca.
        cursor.execute(
            "INSERT INTO books (title, author, category, publish_year, quantity) "
            "VALUES (%s, %s, %s, %s, %s)",
            (title, author, category, publish_year, quantity)
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
        title        = request.form.get("title", "")
        author       = request.form.get("author", "")
        category     = request.form.get("category", "")
        publish_year = request.form.get("publish_year", "")
        quantity     = request.form.get("quantity", 1)

        cursor.execute(
            "UPDATE books SET title=%s, author=%s, category=%s, "
            "publish_year=%s, quantity=%s WHERE id=%s",
            (title, author, category, publish_year, quantity, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for("books"))

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
    print("⚠️  ATENÇÃO: Rodando versão VULNERÁVEL a SQL Injection!")
    print("    Porta: 5000")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
