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

        
        # VULNERABLE QUERY
        query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{password}'
        """

        print("\n[SQL QUERY]")
        print(query)

        cursor.execute(query)

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid username or password"
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
        total_books=total_books["total"]
    )



# LIST BOOKS
@app.route("/books")
def books():

    if "user_id" not in session:
        return redirect("/")

    search = request.args.get("search", "")

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    
    # VULNERABLE SEARCH
    query = f"""
    SELECT * FROM books
    WHERE title LIKE '%{search}%'
    """

    print("\n[SQL QUERY]")
    print(query)

    cursor.execute(query)

    books = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "books.html",
        books=books,
        username=session["username"],
        role=session["role"]
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

        query = f"""
        INSERT INTO books
        (title, author, category, publish_year, quantity)

        VALUES
        (
            '{title}',
            '{author}',
            '{category}',
            '{publish_year}',
            '{quantity}'
        )
        """

        print("\n[SQL QUERY]")
        print(query)

        cursor.execute(query)

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

        query = f"""
        UPDATE books

        SET
            title = '{title}',
            author = '{author}',
            category = '{category}',
            publish_year = '{publish_year}',
            quantity = '{quantity}'

        WHERE id = {id}
        """

        print("\n[SQL QUERY]")
        print(query)

        cursor.execute(query)

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/books")

    cursor.execute(f"SELECT * FROM books WHERE id = {id}")

    book = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_book.html",
        book=book
    )



# DELETE BOOK
@app.route("/books/delete/<int:id>")
def delete_book(id):

    if "user_id" not in session:
        return redirect("/")

    if session["role"] != "admin":
        return "Access denied"

    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"DELETE FROM books WHERE id = {id}"

    print("\n[SQL QUERY]")
    print(query)

    cursor.execute(query)

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
    app.run(debug=True)