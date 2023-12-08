CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX (username));
