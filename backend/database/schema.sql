
CREATE DATABASE IF NOT EXISTS cpe_database;
USE cpe_database;


CREATE TABLE IF NOT EXISTS cpes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpe_title VARCHAR(500),
    cpe_22_uri TEXT,
    cpe_23_uri TEXT,
    reference_links JSON,
    cpe_22_deprecation_date DATE,
    cpe_23_deprecation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_title (cpe_title(255)),
    INDEX idx_22_date (cpe_22_deprecation_date),
    INDEX idx_23_date (cpe_23_deprecation_date)
);
