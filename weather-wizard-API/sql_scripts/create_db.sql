CREATE DATABASE IF NOT EXISTS `WeatherWizard` DEFAULT CHARACTER SET utf8 COLLATE utf8mb3_general_ci;

USE WeatherWizard;

CREATE TABLE IF NOT EXISTS `users`(
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `api_keys`(
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `api_key` varchar(64) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

