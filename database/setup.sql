USE library_demo;

SELECT
    *
FROM
    books;

SELECT
    *
FROM
    users;

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

-- INSERT USERS
INSERT INTO
    users (username, password, role)
VALUES
    ('admin', 'admin123', 'admin'),
    ('luan', '123456', 'user'),
    ('biblioteca', 'senha123', 'admin');

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
    ),
    (
        'Grande Sertão: Veredas',
        'João Guimarães Rosa',
        'Romance',
        1956,
        3
    ),
    (
        'O Alquimista',
        'Paulo Coelho',
        'Fábula',
        1988,
        12
    ),
    (
        'Admirável Mundo Novo',
        'Aldous Huxley',
        'Ficção Distópica',
        1932,
        6
    ),
    (
        'Fahrenheit 451',
        'Ray Bradbury',
        'Ficção Distópica',
        1953,
        5
    ),
    (
        'O Senhor dos Anéis: A Sociedade do Anel',
        'J.R.R. Tolkien',
        'Fantasia',
        1954,
        9
    ),
    (
        'As Crónicas de Nárnia',
        'C.S. Lewis',
        'Fantasia',
        1950,
        8
    ),
    (
        'Duna',
        'Frank Herbert',
        'Ficção Científica',
        1965,
        4
    ),
    (
        'O Guia do Mochileiro das Galáxias',
        'Douglas Adams',
        'Ficção Científica',
        1979,
        11
    ),
    (
        'Introduction to Algorithms',
        'Thomas H. Cormen',
        'Computação',
        1990,
        3
    ),
    (
        'Design Patterns',
        'Erich Gamma',
        'Tecnologia',
        1994,
        4
    ),
    (
        'Refactoring',
        'Martin Fowler',
        'Tecnologia',
        1999,
        5
    ),
    (
        'O Código Da Vinci',
        'Dan Brown',
        'Suspense',
        2003,
        7
    ),
    (
        'Garotas de Vidro',
        'Laurie Halse Anderson',
        'Drama',
        2009,
        4
    ),
    (
        'Sapiens: Uma Breve História',
        'Yuval Noah Harari',
        'História',
        2011,
        10
    ),
    (
        'Cem Anos de Solidão',
        'Gabriel García Márquez',
        'Realismo Mágico',
        1967,
        6
    ),
    (
        'O Cortiço',
        'Aluísio Azevedo',
        'Clássico',
        1890,
        4
    ),
    (
        'Memórias Póstumas de Brás Cubas',
        'Machado de Assis',
        'Clássico',
        1881,
        7
    ),
    (
        'Iracema',
        'José de Alencar',
        'Romantismo',
        1865,
        3
    ),
    (
        'Macunaíma',
        'Mário de Andrade',
        'Modernismo',
        1928,
        5
    ),
    (
        'Vidas Secas',
        'Graciliano Ramos',
        'Drama',
        1938,
        8
    ),
    (
        'Capitães da Areia',
        'Jorge Amado',
        'Drama',
        1937,
        6
    ),
    (
        'A Hora da Estrela',
        'Clarice Lispector',
        'Romance',
        1977,
        4
    ),
    (
        'O Retrato de Dorian Gray',
        'Oscar Wilde',
        'Clássico',
        1890,
        5
    ),
    ('Frankenstein', 'Mary Shelley', 'Terror', 1818, 6),
    ('Drácula', 'Bram Stoker', 'Terror', 1897, 4),
    (
        'A Metamorfose',
        'Franz Kafka',
        'Filosofia',
        1915,
        9
    ),
    ('O Processo', 'Franz Kafka', 'Ficção', 1925, 3),
    (
        'Assim Falou Zarandustra',
        'Friedrich Nietzsche',
        'Filosofia',
        1883,
        5
    ),
    (
        'O Príncipe',
        'Nicolau Maquiavel',
        'Filosofia',
        1532,
        12
    ),
    ('A República', 'Platão', 'Filosofia', -375, 8),
    (
        'A Arte da Guerra',
        'Sun Tzu',
        'Estratégia',
        -475,
        15
    ),
    (
        'O Estrangeiro',
        'Albert Camus',
        'Existencialismo',
        1942,
        6
    ),
    (
        'Ensaio Sobre a Cegueira',
        'José Saramago',
        'Literatura',
        1995,
        7
    ),
    (
        'Crime e Castigo',
        'Fiódor Dostoiévski',
        'Drama',
        1866,
        4
    ),
    (
        'Os Irmãos Karamazov',
        'Fiódor Dostoiévski',
        'Drama',
        1880,
        2
    ),
    (
        'Guerra e Paz',
        'Lev Tolstói',
        'Romance Histórico',
        1869,
        3
    ),
    (
        'Anna Karenina',
        'Lev Tolstói',
        'Romance',
        1877,
        4
    ),
    (
        'Madame Bovary',
        'Gustave Flaubert',
        'Realismo',
        1856,
        5
    ),
    (
        'Os Miseráveis',
        'Victor Hugo',
        'Clássico',
        1862,
        3
    ),
    (
        'O Corvo e Outros Contos',
        'Edgar Allan Poe',
        'Terror',
        1845,
        6
    ),
    ('O Iluminado', 'Stephen King', 'Terror', 1977, 8),
    ('It: A Coisa', 'Stephen King', 'Terror', 1986, 5),
    ('Misery', 'Stephen King', 'Suspense', 1987, 4),
    (
        'Sherlock Holmes: Um Estudo em Vermelho',
        'Arthur Conan Doyle',
        'Mistério',
        1887,
        10
    ),
    (
        'O Cão dos Baskerville',
        'Arthur Conan Doyle',
        'Mistério',
        1902,
        7
    ),
    (
        'E Não Sobrou Nenhum',
        'Agatha Christie',
        'Mistério',
        1939,
        12
    ),
    (
        'Assassinato no Expresso do Oriente',
        'Agatha Christie',
        'Mistério',
        1934,
        9
    ),
    (
        'Moby Dick',
        'Herman Melville',
        'Aventura',
        1851,
        4
    ),
    (
        'A Ilha do Tesouro',
        'Robert Louis Stevenson',
        'Aventura',
        1883,
        6
    ),
    (
        'O Médico e o Monstro',
        'Robert Louis Stevenson',
        'Clássico',
        1886,
        8
    ),
    (
        'Neuromancer',
        'William Gibson',
        'Cyberpunk',
        1984,
        5
    ),
    (
        'Snow Crash',
        'Neal Stephenson',
        'Cyberpunk',
        1992,
        4
    ),
    (
        'Fundação',
        'Isaac Asimov',
        'Ficção Científica',
        1951,
        7
    ),
    (
        'Eu, Robô',
        'Isaac Asimov',
        'Ficção Científica',
        1950,
        9
    ),
    (
        'O Homem Bicentenário',
        'Isaac Asimov',
        'Ficção Científica',
        1976,
        3
    ),
    (
        'The Pragmatic Programmer',
        'Andrew Hunt',
        'Tecnologia',
        1999,
        6
    ),
    (
        'Clean Architecture',
        'Robert C. Martin',
        'Tecnologia',
        2017,
        8
    ),
    (
        'Clean Agile',
        'Robert C. Martin',
        'Tecnologia',
        2019,
        4
    ),
    (
        'Test Driven Development',
        'Kent Beck',
        'Tecnologia',
        2002,
        5
    ),
    (
        'Domain-Driven Design',
        'Eric Evans',
        'Tecnologia',
        2003,
        3
    ),
    (
        'Working Effectively with Legacy Code',
        'Michael Feathers',
        'Tecnologia',
        2004,
        4
    ),
    (
        'Code Complete',
        'Steve McConnell',
        'Tecnologia',
        2004,
        2
    ),
    (
        'The Phoenix Project',
        'Gene Kim',
        'DevOps',
        2013,
        7
    ),
    (
        'The DevOps Handbook',
        'Gene Kim',
        'DevOps',
        2016,
        5
    ),
    (
        'Site Reliability Engineering',
        'Betsy Beyer',
        'DevOps',
        2016,
        6
    ),
    (
        'Continuous Delivery',
        'Jez Humble',
        'Tecnologia',
        2010,
        4
    ),
    (
        'Designing Data-Intensive Applications',
        'Martin Kleppmann',
        'Computação',
        2017,
        8
    ),
    (
        'Cracking the Coding Interview',
        'Gayle Laakmann',
        'Computação',
        2015,
        12
    ),
    (
        'Introduction to Quantum Computing',
        'Phillip Kaye',
        'Computação',
        2007,
        2
    ),
    (
        'Artificial Intelligence: A Modern Approach',
        'Stuart Russell',
        'Computação',
        2009,
        3
    ),
    (
        'Computer Networking',
        'James Kurose',
        'Redes',
        2012,
        5
    ),
    (
        'Modern Operating Systems',
        'Andrew Tanenbaum',
        'Computação',
        2014,
        4
    ),
    (
        'Computer Architecture',
        'John L. Hennessy',
        'Computação',
        2011,
        3
    ),
    (
        'Compiladores: Princípios e Técnicas',
        'Alfred Aho',
        'Computação',
        2006,
        2
    ),
    (
        'O Nome do Vento',
        'Patrick Rothfuss',
        'Fantasia',
        2007,
        8
    ),
    (
        'O Temor do Homem Sábio',
        'Patrick Rothfuss',
        'Fantasia',
        2011,
        6
    ),
    (
        'A Guerra dos Tronos',
        'George R.R. Martin',
        'Fantasia',
        1996,
        11
    ),
    (
        'A Fúria dos Reis',
        'George R.R. Martin',
        'Fantasia',
        1998,
        7
    ),
    (
        'A Tormenta de Espadas',
        'George R.R. Martin',
        'Fantasia',
        2000,
        8
    ),
    (
        'O Festim dos Corvos',
        'George R.R. Martin',
        'Fantasia',
        2005,
        5
    ),
    (
        'A Dança dos Dragões',
        'George R.R. Martin',
        'Fantasia',
        2011,
        6
    ),
    (
        'Percy Jackson: O Ladrão de Raios',
        'Rick Riordan',
        'Fantasia',
        2005,
        10
    ),
    (
        'O Mar de Monstros',
        'Rick Riordan',
        'Fantasia',
        2006,
        8
    ),
    (
        'Jogos Vorazes',
        'Suzanne Collins',
        'Ficção Distópica',
        2008,
        9
    ),
    (
        'Em Chamas',
        'Suzanne Collins',
        'Ficção Distópica',
        2009,
        7
    ),
    (
        'A Esperança',
        'Suzanne Collins',
        'Ficção Distópica',
        2010,
        8
    ),
    (
        'Divergente',
        'Veronica Roth',
        'Ficção Distópica',
        2011,
        6
    ),
    (
        'Homo Deus',
        'Yuval Noah Harari',
        'História',
        2015,
        7
    ),
    (
        '21 Lições para o Século XXI',
        'Yuval Noah Harari',
        'História',
        2018,
        5
    ),
    (
        'O Gene Egoísta',
        'Richard Dawkins',
        'Ciência',
        1976,
        4
    ),
    (
        'Uma Breve História do Tempo',
        'Stephen Hawking',
        'Ciência',
        1988,
        8
    ),
    ('Cosmos', 'Carl Sagan', 'Ciência', 1980, 9),
    (
        'O Mundo Assombrado pelos Demônios',
        'Carl Sagan',
        'Ciência',
        1995,
        6
    ),
    (
        'Blink: O Poder de Pensar Sem Pensar',
        'Malcolm Gladwell',
        'Psicologia',
        2005,
        5
    ),
    (
        'Outliers: Os Fora de Série',
        'Malcolm Gladwell',
        'Psicologia',
        2008,
        6
    ),
    (
        'Rápido e Devagar: Duas Formas de Pensar',
        'Daniel Kahneman',
        'Psicologia',
        2011,
        7
    ),
    (
        'O Poder do Hábito',
        'Charles Duhigg',
        'Autoajuda',
        2012,
        10
    ),
    (
        'Pai Rico, Pai Pobre',
        'Robert Kiyosaki',
        'Finanças',
        1997,
        14
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