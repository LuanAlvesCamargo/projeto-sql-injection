# ============================================================
# db_config.py - VERSÃO SEGURA
# Configuração de conexão com o banco de dados MariaDB
# ============================================================

import mysql.connector

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "root123",
    "database": "library_demo",
}


def get_connection():
    """Retorna uma conexão ativa com o banco de dados."""
    return mysql.connector.connect(**DB_CONFIG)
