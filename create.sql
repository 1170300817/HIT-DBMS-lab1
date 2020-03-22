-- SET NAMES utf8mb4;
-- SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
-- SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
-- SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

-- 
-- Create Database
-- 

DROP SCHEMA IF EXISTS lab1;
CREATE SCHEMA lab1;
USE lab1;

-- 
-- Table structure for table 'actor'
-- 

CREATE TABLE actor(
 actor_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 firstName VARCHAR(45) NOT NULL,
 secondName VARCHAR(45) NOT NULL,
 PRIMARY KEY (actor_id)
);

-- 
-- Table structure for table 'director'
-- 

CREATE TABLE director(
 dir_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 firstName VARCHAR(45) NOT NULL,
 secondName VARCHAR(45) NOT NULL,
 PRIMARY KEY (dir_id)
);

-- 
-- Table structure for table 'user'
-- 

CREATE TABLE user(
 user_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 firstName VARCHAR(45) NOT NULL,
 secondName VARCHAR(45) NOT NULL,
 favorType VARCHAR(45),
 userName VARCHAR(12) UNIQUE NOT NULL,
 password VARCHAR(6) NOT NULL,
 PRIMARY KEY (user_id)
);


-- 
-- Table structure for table 'film'
-- 

CREATE TABLE film(
 film_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
 title VARCHAR(128) NOT NULL,
 type VARCHAR(45),
 director SMALLINT UNSIGNED NOT NULL,
 time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (film_id),
 FOREIGN KEY (director) REFERENCES director(dir_id)
);

-- 
-- Table structure for table 'act'
-- 

CREATE TABLE act(
 actor_id SMALLINT UNSIGNED NOT NULL,
 film_id SMALLINT UNSIGNED NOT NULL,
 PRIMARY KEY (actor_id, film_id),
 FOREIGN KEY (actor_id) REFERENCES actor(actor_id),
 FOREIGN KEY (film_id) REFERENCES film(film_id)
);


-- 
-- Table structure for table 'review'
-- 

CREATE TABLE review(
 film_id SMALLINT UNSIGNED NOT NULL,
 user_id SMALLINT UNSIGNED NOT NULL,
 review TEXT NOT NULL,
 ranked TINYINT UNSIGNED NOT NULL,
 time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (film_id, user_id),
 FOREIGN KEY (film_id) REFERENCES film(film_id),
 FOREIGN KEY (user_id) REFERENCES user(user_id)
);


-- 
-- Table structure for table 'recommend'
-- 

CREATE TABLE recommend(
 referee_id SMALLINT UNSIGNED NOT NULL,
 recommended_id SMALLINT UNSIGNED NOT NULL,
 film_id SMALLINT UNSIGNED NOT NULL,
 PRIMARY KEY (referee_id, recommended_id, film_id),
 FOREIGN KEY (referee_id) REFERENCES user(user_id),
 FOREIGN KEY (recommended_id) REFERENCES user(user_id),
 FOREIGN KEY (film_id) REFERENCES film(film_id)
);


-- 
-- Table structure for table 'watch'
-- 

CREATE TABLE watch(
 user_id SMALLINT UNSIGNED NOT NULL,
 film_id SMALLINT UNSIGNED NOT NULL,
 PRIMARY KEY (user_id, film_id),
 FOREIGN KEY (film_id) REFERENCES film(film_id),
 FOREIGN KEY (user_id) REFERENCES user(user_id)
);














