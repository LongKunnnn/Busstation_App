CREATE DATABASE  IF NOT EXISTS `busstationmanagement` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `busstationmanagement`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignment` (
  `AssignmentID` varchar(10) NOT NULL,
  `BusID` varchar(10) DEFAULT NULL,
  `DriverID` varchar(10) DEFAULT NULL,
  `RouteID` varchar(10) DEFAULT NULL,
  `AssignmentDate` date NOT NULL,
  PRIMARY KEY (`AssignmentID`),
  KEY `BusID` (`BusID`),
  KEY `DriverID` (`DriverID`),
  KEY `RouteID` (`RouteID`),
  CONSTRAINT `assignment_ibfk_1` FOREIGN KEY (`BusID`) REFERENCES `bus` (`BusID`),
  CONSTRAINT `assignment_ibfk_2` FOREIGN KEY (`DriverID`) REFERENCES `driver` (`DriverID`),
  CONSTRAINT `assignment_ibfk_3` FOREIGN KEY (`RouteID`) REFERENCES `route` (`RouteID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignment`
--

LOCK TABLES `assignment` WRITE;
/*!40000 ALTER TABLE `assignment` DISABLE KEYS */;
INSERT INTO `assignment` VALUES ('A001','B001','D001','R001','2024-01-01'),('A002','B002','D002','R002','2024-01-04'),('A003','B003','D003','R003','2024-01-07'),('A004','B004','D004','R004','2024-01-10'),('A005','B005','D005','R005','2024-02-01'),('A006','B006','D006','R006','2024-02-05'),('A007','B007','D007','R007','2024-02-09'),('A008','B008','D008','R008','2024-03-03'),('A009','B009','D009','R009','2024-03-06'),('A010','B010','D010','R010','2024-04-06'),('A011','B011','D011','R011','2024-04-10'),('A012','B012','D012','R012','2025-01-11'),('A013','B013','D013','R013','2025-01-15'),('A014','B014','D014','R014','2025-04-01'),('A015','B015','D015','R015','2025-08-15');
/*!40000 ALTER TABLE `assignment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:41
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bus`
--

DROP TABLE IF EXISTS `bus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus` (
  `BusID` varchar(10) NOT NULL,
  `PlateNumber` varchar(20) NOT NULL,
  `Capacity` int DEFAULT NULL,
  `BusType` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`BusID`),
  UNIQUE KEY `PlateNumber` (`PlateNumber`),
  CONSTRAINT `bus_chk_1` CHECK ((`Capacity` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus`
--

LOCK TABLES `bus` WRITE;
/*!40000 ALTER TABLE `bus` DISABLE KEYS */;
INSERT INTO `bus` VALUES ('B001','29B-10001',40,'Standard'),('B002','29B-10002',40,'Standard'),('B003','29B-10003',40,'Standard'),('B004','29B-10004',40,'Standard'),('B005','29B-10005',40,'Standard'),('B006','29B-10006',50,'Big'),('B007','29B-10007',50,'Big'),('B008','29B-10008',50,'Big'),('B009','29B-10009',50,'Big'),('B010','29B-10010',50,'Big'),('B011','29B-10011',30,'Mini'),('B012','29B-10012',30,'Mini'),('B013','29B-10013',30,'Mini'),('B014','29B-10014',30,'Mini'),('B015','29B-10015',30,'Mini');
/*!40000 ALTER TABLE `bus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:40
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `busstop`
--

DROP TABLE IF EXISTS `busstop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `busstop` (
  `StopID` varchar(10) NOT NULL,
  `StopName` varchar(100) NOT NULL,
  `Location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`StopID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `busstop`
--

LOCK TABLES `busstop` WRITE;
/*!40000 ALTER TABLE `busstop` DISABLE KEYS */;
INSERT INTO `busstop` VALUES ('S001','Trạm 1','Ngã 3 Trường Chinh'),('S002','Trạm 2','Ngã tư sở'),('S003','Trạm 3','Đại học Quốc Gia'),('S004','Trạm 4','Phạm Văn Đồng'),('S005','Trạm 5','Văn Miếu - Quốc Tử Giám'),('S006','Trạm 6','Nhà Hát Lớn'),('S007','Trạm 7','Lạc Long Quân'),('S008','Trạm 8','Đại lộ Thăng Long'),('S009','Trạm 9','Ngã tư Khuất Duy Tiến'),('S010','Trạm 10','Nguyễn Xiển - Thanh Xuân'),('S011','Trạm 11','Láng Hạ'),('S012','Trạm 12','Nhổn'),('S013','Trạm 13','Văn Quán'),('S014','Trạm 14','Long Biên'),('S015','Trạm 15','Aeon Mall Hà Đông');
/*!40000 ALTER TABLE `busstop` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:41
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `driver` (
  `DriverID` varchar(10) NOT NULL,
  `FullName` varchar(100) NOT NULL,
  `Gender` enum('Nam','Nữ','Khác') DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `PhoneNumber` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`DriverID`),
  UNIQUE KEY `PhoneNumber` (`PhoneNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES ('D001','Nguyễn Văn Dũng','Nam','1980-05-22','0922345671'),('D002','Nguyễn Bảo Nam','Nam','1982-01-20','0952345672'),('D003','Trần Đức Thịnh ','Nam','1988-05-23','0962345673'),('D004','Trịnh Kim Loan','Nữ','1999-05-20','0916345674'),('D005','Lê Văn Tuấn','Nam','1980-08-08','0915345675'),('D006','Vũ Văn Hòa','Nam','1992-05-13','0919345676'),('D007','Vũ Đức Hoàng','Nam','1991-07-09','0912345677'),('D008','Tô Thị Linh','Nữ','1991-01-11','0912345678'),('D009','Trần Quang Phương','Nam','1993-09-12','0912345679'),('D010','Vũ Trọng Nam','Nam','1982-05-01','0912345688'),('D011','Lê Kim Huyền','Nữ','1988-05-20','0912345898'),('D012','Lâm Xung','Nam','1999-11-12','0912345611'),('D013','Tống Giang','Nam','1997-12-26','0912345601'),('D014','Sơn Văn Tùng','Nam','1977-05-11','0913452378'),('D015','Triệu Vân','Nam','1979-04-10','0912345458');
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:40
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `route`
--

DROP TABLE IF EXISTS `route`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `route` (
  `RouteID` varchar(10) NOT NULL,
  `RouteName` varchar(100) NOT NULL,
  `StartPoint` varchar(100) NOT NULL,
  `EndPoint` varchar(100) NOT NULL,
  `Distance` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`RouteID`),
  CONSTRAINT `route_chk_1` CHECK ((`Distance` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `route`
--

LOCK TABLES `route` WRITE;
/*!40000 ALTER TABLE `route` DISABLE KEYS */;
INSERT INTO `route` VALUES ('R001','Tuyến 1','Bến xe A','Bến xe B',15.50),('R002','Tuyến 1','Bến xe A','Bến xe B',16.50),('R003','Tuyến 1','Bến xe A','Bến xe B',17.50),('R004','Tuyến 1','Bến xe A','Bến xe B',18.50),('R005','Tuyến 1','Bến xe A','Bến xe B',19.50),('R006','Tuyến 2','Bến xe B','Bến xe A',15.50),('R007','Tuyến 2','Bến xe B','Bến xe A',15.40),('R008','Tuyến 2','Bến xe B','Bến xe A',15.30),('R009','Tuyến 2','Bến xe B','Bến xe A',17.50),('R010','Tuyến 1','Bến xe A','Bến xe B',11.50),('R011','Tuyến 1','Bến xe A','Bến xe B',14.50),('R012','Tuyến 1','Bến xe A','Bến xe B',15.50),('R013','Tuyến 2','Bến xe B','Bến xe A',15.40),('R014','Tuyến 2','Bến xe B','Bến xe A',15.30),('R015','Tuyến 1','Bến xe A','Bến xe B',15.50);
/*!40000 ALTER TABLE `route` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:41
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `route_stop`
--

DROP TABLE IF EXISTS `route_stop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `route_stop` (
  `RouteID` varchar(10) NOT NULL,
  `StopID` varchar(10) DEFAULT NULL,
  `StopOrder` int NOT NULL,
  PRIMARY KEY (`RouteID`,`StopOrder`),
  KEY `StopID` (`StopID`),
  CONSTRAINT `route_stop_ibfk_1` FOREIGN KEY (`RouteID`) REFERENCES `route` (`RouteID`),
  CONSTRAINT `route_stop_ibfk_2` FOREIGN KEY (`StopID`) REFERENCES `busstop` (`StopID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `route_stop`
--

LOCK TABLES `route_stop` WRITE;
/*!40000 ALTER TABLE `route_stop` DISABLE KEYS */;
INSERT INTO `route_stop` VALUES ('R001','S001',1),('R005','S001',1),('R008','S001',1),('R013','S001',1),('R001','S002',2),('R006','S002',1),('R009','S002',3),('R015','S002',1),('R001','S003',3),('R005','S003',2),('R007','S003',1),('R011','S003',1),('R001','S004',4),('R006','S004',2),('R010','S004',1),('R013','S004',2),('R002','S005',1),('R005','S005',3),('R007','S005',2),('R009','S005',4),('R012','S005',1),('R015','S005',2),('R002','S006',2),('R008','S006',2),('R010','S006',2),('R014','S006',1),('R002','S007',3),('R005','S007',4),('R006','S007',3),('R011','S007',2),('R002','S008',4),('R007','S008',3),('R010','S008',4),('R013','S008',3),('R003','S009',1),('R006','S009',4),('R011','S009',3),('R014','S009',2),('R007','S010',4),('R012','S010',2),('R014','S010',4),('R003','S011',2),('R004','S011',4),('R008','S011',3),('R011','S011',4),('R015','S011',3),('R003','S012',3),('R004','S012',2),('R008','S012',4),('R012','S012',3),('R009','S013',1),('R014','S013',3),('R004','S014',1),('R010','S014',3),('R012','S014',4),('R015','S014',4),('R003','S015',4),('R004','S015',3),('R009','S015',2),('R013','S015',4);
/*!40000 ALTER TABLE `route_stop` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:41
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `ScheduleID` varchar(10) NOT NULL,
  `RouteID` varchar(10) DEFAULT NULL,
  `DepartureTime` time NOT NULL,
  `ArrivalTime` time NOT NULL,
  `DayOfWeek` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') DEFAULT NULL,
  PRIMARY KEY (`ScheduleID`),
  KEY `RouteID` (`RouteID`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`RouteID`) REFERENCES `route` (`RouteID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES ('SCH001','R001','06:00:00','07:00:00','Monday'),('SCH002','R002','06:30:00','07:40:00','Tuesday'),('SCH003','R003','07:00:00','08:00:00','Wednesday'),('SCH004','R004','07:30:00','08:45:00','Thursday'),('SCH005','R005','08:00:00','09:10:00','Friday'),('SCH006','R006','08:30:00','09:30:00','Saturday'),('SCH007','R007','09:00:00','10:10:00','Sunday'),('SCH008','R008','09:30:00','10:30:00','Monday'),('SCH009','R009','10:00:00','11:00:00','Tuesday'),('SCH010','R010','10:30:00','11:45:00','Wednesday'),('SCH011','R011','11:00:00','12:00:00','Thursday'),('SCH012','R012','11:30:00','12:45:00','Friday'),('SCH013','R013','12:00:00','13:00:00','Saturday'),('SCH014','R014','12:30:00','13:30:00','Sunday'),('SCH015','R015','13:00:00','14:10:00','Monday');
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:40
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: busstationmanagement
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'busstationmanagement'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-18 20:35:41
