# 📚 projeto-sql-injection

Sistema de biblioteca didático para **demonstração de SQL Injection** e sua mitigação com Prepared Statements.

> **⚠️ Aviso:** A versão vulnerável é propositalmente insegura. Use apenas em ambientes locais/acadêmicos.

---

## 🎯 Objetivo

Demonstrar na prática:

1. Como SQL Injection funciona em aplicações reais
2. Por que concatenação de strings em queries é perigosa
3. Como Prepared Statements eliminam essa vulnerabilidade

---

## 🗂️ Estrutura do Projeto

```
projeto-sql-injection/
├── README.md
├── requirements.txt
├── .gitignore
│
├── database/
│   └── setup.sql              ← Script de criação do banco
│
├── vulnerable_app/            ← ⚠️ Versão VULNERÁVEL (porta 5000)
│   ├── app.py
│   ├── db_config.py
│   ├── templates/
│   └── static/
│
└── secure_app/                ← ✅ Versão SEGURA (porta 5001)
    ├── app.py
    ├── db_config.py
    ├── templates/
    └── static/
```

---

## ⚙️ Requisitos

- Python 3.9+
- MariaDB (ou MySQL) rodando localmente
- pip

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repo>
cd projeto-sql-injection
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Certifique-se de que o MariaDB está rodando com:

```
Host:     localhost
Porta:    3306
Usuário:  root
Senha:    root123
```

Execute o script SQL:

```bash
mysql -u root -p < database/setup.sql
```

---

## ▶️ Executar as aplicações

### Versão Vulnerável (porta 5000)

```bash
cd vulnerable_app
python app.py
```

Acesse: [http://localhost:5000](http://localhost:5000)

### Versão Segura (porta 5001)

```bash
cd secure_app
python app.py
```

Acesse: [http://localhost:5001](http://localhost:5001)

> Você pode rodar as duas ao mesmo tempo em terminais diferentes!

---

## 👤 Usuários de Teste

| Usuário | Senha     | Perfil |
|---------|-----------|--------|
| admin   | admin123  | admin  |
| joao    | joao456   | user   |
| maria   | maria789  | user   |
| prof    | prof2024  | admin  |

---

## 💉 Como Demonstrar SQL Injection

### Ataque 1 — Bypass de Login (versão vulnerável)

No campo **Usuário**, insira:
```
' OR '1'='1
```
No campo **Senha**, insira:
```
' OR '1'='1
```

**Query gerada:**
```sql
SELECT * FROM users
WHERE username='' OR '1'='1' AND password='' OR '1'='1'
```

Como `'1'='1'` é sempre verdadeiro, o login é contornado sem credenciais válidas.

---

### Ataque 2 — Comentário SQL

No campo **Usuário**, insira:
```
admin'--
```
No campo **Senha**, insira qualquer coisa.

**Query gerada:**
```sql
SELECT * FROM users WHERE username='admin'--' AND password='...'
```

O `--` comenta o restante da query, ignorando a verificação de senha.

---

### Ataque 3 — Busca Maliciosa

Na página de livros, busque por:
```
%' OR '1'='1
```

**Query gerada:**
```sql
SELECT * FROM books WHERE title LIKE '%%' OR '1'='1%'
```

Retorna **todos** os registros da tabela, ignorando o filtro de título.

---

## 🛡️ Como a Versão Segura Bloqueia Esses Ataques

### Prepared Statements

```python
# ❌ VULNERÁVEL — concatenação direta
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)

# ✅ SEGURO — prepared statement
cursor.execute(
    "SELECT * FROM users WHERE username=%s AND password=%s",
    (username, password)
)
```

Com Prepared Statements, o banco recebe a query e os parâmetros **separadamente**. Qualquer caractere especial no input (como aspas simples) é tratado como dado literal, nunca como instrução SQL.

Se o usuário digitar `' OR '1'='1`, o banco procura literalmente por um usuário chamado `' OR '1'='1` — que não existe.

### Validação de Entrada

A versão segura também valida os dados antes de enviar ao banco:

```python
def is_valid_year(year):
    try:
        return 1800 <= int(year) <= 2099
    except:
        return False
```

---

## 📊 Comparativo

| Aspecto                 | Versão Vulnerável        | Versão Segura              |
|-------------------------|--------------------------|----------------------------|
| Construção da query     | f-string / concatenação  | Prepared statements (%s)   |
| Login bypass            | ✅ Funciona              | ❌ Bloqueado               |
| Injeção na busca        | ✅ Funciona              | ❌ Bloqueado               |
| Validação de campos     | Não                      | Sim                        |
| Senha no formulário     | type="text" (exposta)    | type="password"            |
| Interface               | Tema vermelho (alerta)   | Tema verde (segurança)     |
| Porta padrão            | 5000                     | 5001                       |

---

## 🎓 Roteiro de Apresentação Acadêmica

1. **Contexte o problema** — mostre o código vulnerável com `print()` da query no terminal
2. **Execute o bypass** — entre com `' OR '1'='1` e mostre o acesso indevido
3. **Execute a busca maliciosa** — mostre todos os registros expostos
4. **Mude para a versão segura** — tente os mesmos payloads e mostre que não funcionam
5. **Explique o porquê** — compare os dois trechos de código lado a lado
6. **Conclusão** — sempre use Prepared Statements em produção

---

## 📦 Dependências

```
flask==3.0.0
mysql-connector-python==8.2.0
```

---

## 📄 Licença

Projeto acadêmico — uso livre para fins educacionais.
