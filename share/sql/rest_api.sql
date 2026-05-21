SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Database: `rest_api`
CREATE DATABASE IF NOT EXISTS `rest_api` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `rest_api`;

-- Table `user`
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(32) NOT NULL,
    `email` varchar(320) NOT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table `task`
DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
    `task_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `title` varchar(128) NOT NULL,
    `description` text NOT NULL,
    `creation_date` datetime NOT NULL,
    `status` tinyint(3) NOT NULL DEFAULT 1,
    PRIMARY KEY (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table `user_task` (pivot)
DROP TABLE IF EXISTS `user_task`;
CREATE TABLE `user_task` (
    `user_id` int(11) unsigned NOT NULL,
    `task_id` int(11) unsigned NOT NULL,
    UNIQUE KEY `user_task_unique` (`user_id`, `task_id`),
    KEY `fk_user_task_user` (`user_id`),
    KEY `fk_user_task_task` (`task_id`),
    CONSTRAINT `fk_user_task_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_task_task` FOREIGN KEY (`task_id`) REFERENCES `task` (`task_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed data
INSERT INTO `user` (`user_id`, `name`, `email`) VALUES
(1, 'G4', 'g4@example.com');

INSERT INTO `task` (`task_id`, `title`, `description`, `creation_date`, `status`) VALUES
(1, 'Task 1', 'Description of task 1', NOW(), 1),
(2, 'Task 2', 'Description of task 2', NOW(), 2);

INSERT INTO `user_task` (`user_id`, `task_id`) VALUES
(1, 1),
(1, 2);

SET FOREIGN_KEY_CHECKS = 1;
