CREATE DATABASE IF NOT EXISTS ponto_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ponto_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'funcionaria') NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    data DATE NOT NULL,
    hora_entrada TIME DEFAULT NULL,
    hora_saida TIME DEFAULT NULL,
    observacoes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;