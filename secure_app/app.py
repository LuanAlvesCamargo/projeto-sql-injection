import os

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect, session, url_for
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # CORREÇÃO: Usando %s como placeholders e passando os valores em uma tupla
        query = """
        SELECT * FROM users 
        WHERE username = %s 
        AND password = %s
        """

        print("\n[SQL QUERY SECURE]")
        print(query)

        # O cursor recebe a query e a tupla com os parâmetros organizados
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect("/dashboard")

        return render_template(
            "login.html", error="Invalid username or password"
        )

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM books")
    total_books = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"],
        total_books=total_books["total"],
    )


# LIST BOOKS
@app.route("/books")
def books():
    if "user_id" not in session:
        return redirect("/")

    search = request.args.get("search", "")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # CORREÇÃO: Para o LIKE, colocamos os '%' dentro do valor do parâmetro, não na query
    query = """
    SELECT * FROM books 
    WHERE title LIKE %s
    """
    search_param = f"%{search}%"

    print("\n[SQL QUERY SECURE]")
    print(query)

    cursor.execute(query, (search_param,))
    books = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "books.html",
        books=books,
        username=session["username"],
        role=session["role"],
    )


# ADD BOOK
@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return "Access denied"

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        publish_year = request.form["publish_year"]
        quantity = request.form["quantity"]

        connection = get_db_connection()
        cursor = connection.cursor()

        # CORREÇÃO: Removidas as f-strings e as aspas simples ao redor dos %s
        query = """
        INSERT INTO books 
        (title, author, category, publish_year, quantity) 
        VALUES (%s, %s, %s, %s, %s)
        """

        print("\n[SQL QUERY SECURE]")
        print(query)

        cursor.execute(
            query, (title, author, category, publish_year, quantity)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/books")

    return render_template("add_book.html")


# EDIT BOOK
@app.route("/books/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return "Access denied"

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        publish_year = request.form["publish_year"]
        quantity = request.form["quantity"]

        # CORREÇÃO: Atualizado para usar parâmetros no SET e no WHERE
        query = """
        UPDATE books 
        SET title = %s, author = %s, category = %s, publish_year = %s, quantity = %s 
        WHERE id = %s
        """

        print("\n[SQL QUERY SECURE]")
        print(query)

        cursor.execute(
            query, (title, author, category, publish_year, quantity, id)
        )
        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/books")

    # CORREÇÃO: Mesmo o ID vindo da URL como int, parametrizar previne falhas futuras
    query_select = "SELECT * FROM books WHERE id = %s"
    cursor.execute(query_select, (id,))
    book = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit_book.html", book=book)


# DELETE BOOK
@app.route("/books/delete/<int:id>")
def delete_book(id):
    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return "Access denied"

    connection = get_db_connection()
    cursor = connection.cursor()

    # CORREÇÃO: Parametrizando a query de remoção
    query = "DELETE FROM books WHERE id = %s"

    print("\n[SQL QUERY SECURE]")
    print(query)

    cursor.execute(query, (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/books")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True, port=5001)