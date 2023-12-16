CREATE TABLE IF NOT EXISTS tasks(
            id INT PRIMARY KEY AUTO_INCREMENT,
            taskname VARCHAR(100) UNIQUE,
            description VARCHAR(500),
            category VARCHAR(100),
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX (taskname));
