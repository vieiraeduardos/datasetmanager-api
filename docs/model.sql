CREATE DATABASE  IF NOT EXISTS `datasetmanagerdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `datasetmanagerdb`;
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: datasetmanagerdb
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Actors`
--

DROP TABLE IF EXISTS `Actors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Actors` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `Persons_code` int(11) DEFAULT NULL,
  PRIMARY KEY (`code`),
  KEY `fk_Actors_Persons1_idx` (`Persons_code`),
  CONSTRAINT `fk_Actors_Persons1` FOREIGN KEY (`Persons_code`) REFERENCES `Persons` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Actors`
--

LOCK TABLES `Actors` WRITE;
/*!40000 ALTER TABLE `Actors` DISABLE KEYS */;
INSERT INTO `Actors` VALUES (34,'Maria','maria@gmail.com',5),(35,'João','joao@gmail.com',6),(47,'Maria','maria@gmail.com',5),(48,'João','joao@gmail.com',6);
/*!40000 ALTER TABLE `Actors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Annotations`
--

DROP TABLE IF EXISTS `Annotations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Annotations`
--

LOCK TABLES `Annotations` WRITE;
/*!40000 ALTER TABLE `Annotations` DISABLE KEYS */;
INSERT INTO `Annotations` VALUES (58,12,34,28,20,717,719,80,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/80.jpg'),(59,12,34,28,20,717,719,80,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/80.jpg'),(61,12,34,81,27,748,719,120,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/120.jpg'),(62,12,35,648,0,1277,719,120,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/120.jpg'),(63,12,35,647,0,1271,719,140,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/140.jpg'),(65,12,35,674,0,1279,719,160,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/160.jpg'),(67,12,35,659,0,1279,719,180,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/180.jpg'),(68,12,34,138,20,774,719,200,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/200.jpg'),(69,12,35,660,0,1279,719,200,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/200.jpg'),(70,12,34,134,9,770,719,220,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/220.jpg'),(71,12,35,659,0,1279,719,220,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/220.jpg'),(74,12,35,637,0,1263,719,240,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/240.jpg'),(75,12,34,92,18,717,719,260,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/260.jpg'),(77,12,35,631,0,1261,719,260,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/260.jpg'),(78,12,34,99,20,718,719,280,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/280.jpg'),(79,12,34,99,20,718,719,280,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/280.jpg'),(80,12,35,631,0,1261,719,280,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/280.jpg'),(81,12,34,105,23,714,719,300,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/300.jpg'),(83,12,35,635,0,1266,719,300,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/300.jpg'),(111,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_240.jpg'),(112,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_240.jpg'),(113,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_90.jpg'),(114,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_90.jpg'),(115,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_150.jpg'),(116,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_150.jpg'),(117,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_30.jpg'),(118,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_30.jpg'),(119,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_270.jpg'),(120,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_270.jpg'),(121,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_210.jpg'),(122,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_210.jpg'),(123,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_120.jpg'),(124,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_120.jpg'),(125,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_60.jpg'),(126,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_60.jpg'),(127,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_300.jpg'),(128,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_300.jpg'),(129,20,48,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_180.jpg'),(130,20,47,0,0,0,0,0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/frame_180.jpg');
/*!40000 ALTER TABLE `Annotations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Persons`
--

DROP TABLE IF EXISTS `Persons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Persons` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Persons`
--

LOCK TABLES `Persons` WRITE;
/*!40000 ALTER TABLE `Persons` DISABLE KEYS */;
INSERT INTO `Persons` VALUES (3,'Eduardo','eduardo@gmail.com','static/profile_photos/eduardo.jpg'),(4,'Jane','jane@example.com','static/profile_photos/default-avatar.png'),(5,'Maria','maria@gmail.com','static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/34/80.jpg'),(6,'João','joao@gmail.com','static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/35/240.jpg');
/*!40000 ALTER TABLE `Persons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Videos`
--

DROP TABLE IF EXISTS `Videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Videos` (
  `code` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `tags` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Videos`
--

LOCK TABLES `Videos` WRITE;
/*!40000 ALTER TABLE `Videos` DISABLE KEYS */;
INSERT INTO `Videos` VALUES (12,'$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK',1,'static/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK/$2b$14$qS3wjecSyt18s3fYK2zqie3KsVYBqvYlfsdilp4v9azzlE30SKnK.mp4',''),(20,'Descomplica.mp4',0,'static/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi/$2b$14$0jCHfABT26HKYoskJodO8OzSVEqwsxS4eK5rzfFoeP5t9JP4lLhi.mp4','');
/*!40000 ALTER TABLE `Videos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-26 19:22:34
