CREATE DATABASE  IF NOT EXISTS `datasetmanagerdb`;

USE `datasetmanagerdb`;

DROP TABLE IF EXISTS `Persons`;
CREATE TABLE `Persons` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`)
);

DROP TABLE IF EXISTS `Actors`;

CREATE TABLE `Actors` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `Persons_code` int(11) DEFAULT NULL,
  PRIMARY KEY (`code`),
  KEY `fk_Actors_Persons1_idx` (`Persons_code`),
  CONSTRAINT `fk_Actors_Persons1` FOREIGN KEY (`Persons_code`) REFERENCES `Persons` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS `Videos`;

CREATE TABLE `Videos` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `tags` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`code`)
);

DROP TABLE IF EXISTS `Annotations`;

CREATE TABLE `Annotations` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `Videos_code` int(11) DEFAULT NULL,
  `Actors_code` int(11) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `w` int(11) DEFAULT NULL,
  `h` int(11) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`),
  KEY `fk_Actors_has_Videos_Videos1_idx` (`Videos_code`),
  KEY `fk_Actors_has_Videos_Actors_idx` (`Actors_code`),
  CONSTRAINT `fk_Actors_has_Videos_Actors` FOREIGN KEY (`Actors_code`) REFERENCES `Actors` (`code`),
  CONSTRAINT `fk_Actors_has_Videos_Videos1` FOREIGN KEY (`Videos_code`) REFERENCES `Videos` (`code`)
);