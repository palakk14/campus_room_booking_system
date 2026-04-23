CREATE DATABASE IF NOT EXISTS campus_booking;
USE campus_booking;

-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    password VARCHAR(255) DEFAULT NULL,
    role VARCHAR(20) DEFAULT NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (user_id),
    UNIQUE KEY email (email)
);

-- =========================
-- ROOMS TABLE
-- =========================
CREATE TABLE rooms (
    room_id INT NOT NULL AUTO_INCREMENT,
    room_name VARCHAR(100) DEFAULT NULL,
    capacity INT DEFAULT NULL,
    type VARCHAR(50) DEFAULT NULL,
    status VARCHAR(20) DEFAULT NULL,

    PRIMARY KEY (room_id)
);

-- =========================
-- BOOKINGS TABLE
-- =========================
CREATE TABLE bookings (
    booking_id INT NOT NULL AUTO_INCREMENT,
    user_id INT DEFAULT NULL,
    room_id INT DEFAULT NULL,
    date DATE DEFAULT NULL,
    start_time TIME DEFAULT NULL,
    end_time TIME DEFAULT NULL,
    purpose VARCHAR(255) DEFAULT NULL,
    status VARCHAR(20) DEFAULT NULL,

    PRIMARY KEY (booking_id),

    KEY user_id (user_id),
    KEY room_id (room_id),

    CONSTRAINT bookings_ibfk_1
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT bookings_ibfk_2
        FOREIGN KEY (room_id)
        REFERENCES rooms(room_id)
);