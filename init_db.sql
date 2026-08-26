-- Luodaan tietokanta (jos sitä ei ole) ja otetaan se käyttöön
CREATE DATABASE IF NOT EXISTS mini_tms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mini_tms_db;

-- 1. Ajoneuvot-taulu
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(10) NOT NULL UNIQUE,
    capacity_kg INT,
    status VARCHAR(20) DEFAULT 'AVAILABLE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Kuljetukset-taulu
CREATE TABLE deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT,
    destination_address VARCHAR(255) NOT NULL,
    postal_code VARCHAR(5) NOT NULL,
    price DECIMAL(10, 2),
    raw_message TEXT,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- 3. Telematiikka-taulu (GPS-seuranta)
CREATE TABLE telematics_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);