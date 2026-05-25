-- SQL INJECTION DEMO - LIBRARY SYSTEM
-- DATABASE SETUP SCRIPT
-- REMOVE DATABASE IF EXISTS
DROP DATABASE IF EXISTS library_demo;

-- CREATE DATABASE
CREATE DATABASE library_demo;

-- SELECT DATABASE
USE library_demo;

-- TABLE: USERS
CREATE TABLE
    users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        role ENUM ('admin', 'user') NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- TABLE: BOOKS
CREATE TABLE
    books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        category VARCHAR(100),
        publish_year INT,
        quantity INT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- INSERT USERS
INSERT INTO
    users (username, password, role)
VALUES
    ('admin', 'admin123', 'admin'),
    ('luan', '123456', 'user'),
    ('biblioteca', 'senha123', 'admin');

-- INSERT BOOKS
INSERT INTO
    books (title, author, category, publish_year, quantity)
VALUES
    (
        'Dom Casmurro',
        'Machado de Assis',
        'Romance',
        1899,
        5
    ),
    (
        '1984',
        'George Orwell',
        'Ficção Distópica',
        1949,
        8
    ),
    (
        'O Hobbit',
        'J.R.R. Tolkien',
        'Fantasia',
        1937,
        10
    ),
    (
        'Clean Code',
        'Robert C. Martin',
        'Tecnologia',
        2008,
        4
    ),
    (
        'Harry Potter e a Pedra Filosofal',
        'J.K. Rowling',
        'Fantasia',
        1997,
        7
    ),
    (
        'O Pequeno Príncipe',
        'Antoine de Saint-Exupéry',
        'Fábula',
        1943,
        6
    ),
    (
        'Algoritmos',
        'Thomas H. Cormen',
        'Computação',
        2009,
        2
    );

-- VALIDATION
SELECT
    *
FROM
    users;

SELECT
    *
FROM
    books;