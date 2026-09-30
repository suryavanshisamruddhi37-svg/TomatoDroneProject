CREATE DATABASE IF NOT EXISTS crop_disease_db;
USE crop_disease_db;

CREATE TABLE IF NOT EXISTS crops (
    crop_id INT PRIMARY KEY AUTO_INCREMENT,
    crop_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS diseases (
    disease_id INT PRIMARY KEY AUTO_INCREMENT,
    disease_name VARCHAR(100) NOT NULL UNIQUE,
    symptoms TEXT
);

CREATE TABLE IF NOT EXISTS leaf_assessments (
    assessment_id INT PRIMARY KEY AUTO_INCREMENT,
    crop_id INT NOT NULL,
    disease_id INT NULL,
    image_path VARCHAR(255),
    result ENUM('Healthy', 'Infected') NOT NULL,
    confidence DECIMAL(5,2),
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id),
    FOREIGN KEY (disease_id) REFERENCES diseases(disease_id),
    CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 100))
);

CREATE TABLE IF NOT EXISTS quality_assessments (
    quality_id INT PRIMARY KEY AUTO_INCREMENT,
    crop_id INT NOT NULL,
    image_path VARCHAR(255),
    quality_grade ENUM('A', 'B', 'C', 'Rejected') NULL,
    notes TEXT,
    infection_percentage DECIMAL(5,2) NULL,
    severity VARCHAR(20) NULL,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id)
);