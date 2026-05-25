# projeto-sql-injection

Projeto acadêmico desenvolvido em Flask e MariaDB para demonstrar vulnerabilidades SQL Injection, exploração prática e técnicas de mitigação utilizando prepared statements e validação de entrada.

```
projeto-sql-injection/
│
├── README.md
├── requirements.txt
│
├── database/
│   └── setup.sql
│
├── vulnerable_app/
│   ├── app.py
│   ├── db_config.py
│   │
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── books.html
│   │   ├── add_book.html
│   │   └── edit_book.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── script.js
│
├── secure_app/
│   ├── app.py
│   ├── db_config.py
│   │
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── books.html
│   │   ├── add_book.html
│   │   └── edit_book.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           └── script.js
```

# Criar diretorios e arquivos

```
mkdir -p vulnerable_app/templates
mkdir -p vulnerable_app/static/css
mkdir -p vulnerable_app/static/js

mkdir -p secure_app/templates
mkdir -p secure_app/static/css
mkdir -p secure_app/static/js


touch vulnerable_app/app.py
touch vulnerable_app/db_config.py

touch vulnerable_app/templates/login.html
touch vulnerable_app/templates/dashboard.html
touch vulnerable_app/templates/books.html
touch vulnerable_app/templates/add_book.html
touch vulnerable_app/templates/edit_book.html

touch vulnerable_app/static/css/style.css
touch vulnerable_app/static/js/script.js


touch secure_app/app.py
touch secure_app/db_config.py

touch secure_app/templates/login.html
touch secure_app/templates/dashboard.html
touch secure_app/templates/books.html
touch secure_app/templates/add_book.html
touch secure_app/templates/edit_book.html

touch secure_app/static/css/style.css
touch secure_app/static/js/script.js
```

# Criar ambiente virtual (venv)

```
sudo apt update
sudo apt install python3.14-venv

python3 -m venv --clear venv
```
