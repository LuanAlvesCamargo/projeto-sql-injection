-- ============================================================
-- SETUP DO BANCO DE DADOS - library_demo
-- Projeto: Demonstração de SQL Injection
-- ============================================================

-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS library_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE library_demo;

-- ============================================================
-- TABELA DE USUÁRIOS
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABELA DE LIVROS
-- ============================================================
CREATE TABLE IF NOT EXISTS books (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    author       VARCHAR(150) NOT NULL,
    category     VARCHAR(100) NOT NULL,
    publish_year YEAR         NOT NULL,
    quantity     INT          NOT NULL DEFAULT 1,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- DADOS INICIAIS - USUÁRIOS
-- Senhas em texto puro (propositalmente inseguro na versão vulnerável)
-- Na versão segura, deveriam ser hashed com bcrypt
-- ============================================================
INSERT INTO users (username, password, role) VALUES
    ('admin',   'admin123',  'admin'),
    ('joao',    'joao456',   'user'),
    ('maria',   'maria789',  'user'),
    ('prof',    'prof2024',  'admin');

-- ============================================================
-- DADOS INICIAIS - LIVROS
-- ============================================================
INSERT INTO books (title, author, category, publish_year, quantity) VALUES
    ('Clean Code',                          'Robert C. Martin',    'Programação',    2008, 3),
    ('The Pragmatic Programmer',            'Andrew Hunt',         'Programação',    1999, 2),
    ('Design Patterns',                     'Gang of Four',        'Arquitetura',    1994, 1),
    ('Segurança em Aplicações Web',         'Marcus Pinto',        'Segurança',      2007, 4),
    ('SQL Injection Attacks and Defense',   'Justin Clarke',       'Segurança',      2009, 2),
    ('The Web Application Hacker Handbook', 'Dafydd Stuttard',     'Segurança',      2011, 3),
    ('Introduction to Algorithms',          'Cormen et al.',       'Algoritmos',     2009, 2),
    ('Computer Networks',                   'Andrew Tanenbaum',    'Redes',          2010, 5),
    ('Database System Concepts',            'Silberschatz et al.', 'Banco de Dados', 2019, 3),
    ('Operating System Concepts',           'Silberschatz et al.', 'Sistemas',       2018, 4);

-- ============================================================
-- FIM DO SETUP
-- ============================================================
SELECT 'Banco de dados configurado com sucesso!' AS mensagem;
SELECT CONCAT('Usuários criados: ', COUNT(*)) AS info FROM users;
SELECT CONCAT('Livros criados: ',   COUNT(*)) AS info FROM books;
