-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: ponto_db
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `nome`, `username`, `senha`, `tipo`, `telefone`) VALUES (1,'Administrador','raissa','$2b$12$DmpaJhxkDaoGzdWMSy.TkeVhqn073u1dUTxVVGEz6YRn1.LltmUhy','admin','+553175124667');
INSERT INTO `users` (`id`, `nome`, `username`, `senha`, `tipo`, `telefone`) VALUES (7,'Maísa','Maisa','$2b$12$glGGLl.i4k9JYXYf8N18A.Hiup/vkiQH0NrnciuQXMo/MrRtLlqaa','funcionaria','+553191932116');
INSERT INTO `users` (`id`, `nome`, `username`, `senha`, `tipo`, `telefone`) VALUES (8,'Irlaine','Irlaine','$2b$12$J5OxGrp8qjLNw5yBGOw21um19jREtQ7N5pbgvKUdYyhRGDQQVMpdC','funcionaria','+553188179900');
INSERT INTO `users` (`id`, `nome`, `username`, `senha`, `tipo`, `telefone`) VALUES (9,'Teste','Teste','$2b$12$gvEBbySTJt59Hf1BaQ4NouLHdzTxaaxTKA/PPinhLGmYon.m.OzLy','funcionaria','+553191909665');
INSERT INTO `users` (`id`, `nome`, `username`, `senha`, `tipo`, `telefone`) VALUES (10,'Teste1','Teste01','$2b$12$nNVgwQdO54qJ9Ul9s9tnLOE1n3dCTCI4MxBp1o4T8kMJpIeIpiyeG','funcionaria','+553193731622');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (1,7,'2025-09-01','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (2,7,'2025-09-02','08:05:00','18:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (3,7,'2025-09-03','08:05:00','18:13:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (4,7,'2025-09-04','08:09:00','18:13:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (5,7,'2025-09-05','08:14:00','18:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (6,7,'2025-09-06','08:00:00','14:23:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (7,7,'2025-09-08','08:08:00','18:16:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (8,7,'2025-09-09','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (9,7,'2025-09-10','08:00:00','18:27:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (10,7,'2025-09-11','08:04:00','18:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (11,7,'2025-09-12','08:00:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (12,7,'2025-09-13','08:06:00','14:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (13,7,'2025-09-15','08:08:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (14,7,'2025-09-16','08:15:00','18:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (15,7,'2025-09-17','08:10:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (16,7,'2025-09-18','08:10:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (17,7,'2025-09-19','08:08:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (18,7,'2025-09-20','08:00:00','14:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (19,7,'2025-09-22','08:05:00','18:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (20,7,'2025-09-23','08:09:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (21,7,'2025-09-24','08:00:00','18:14:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (22,7,'2025-09-25','08:10:00','18:13:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (23,7,'2025-09-26','08:09:00','18:11:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (24,7,'2025-09-27','08:10:00','14:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (25,7,'2025-09-29','08:02:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (26,7,'2025-09-30','08:10:00','18:13:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (27,8,'2025-07-29','18:00:00','21:45:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (28,8,'2025-07-31','18:00:00','21:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (29,8,'2025-08-01','18:08:08','21:44:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (30,8,'2025-08-02','14:03:00','22:04:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (31,8,'2025-08-04','18:02:00','21:23:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (32,8,'2025-08-05','18:05:00','21:29:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (33,8,'2025-08-06','18:05:00','21:29:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (34,8,'2025-08-07','18:04:01','21:31:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (35,8,'2025-08-08','18:03:00','21:23:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (36,8,'2025-08-10','08:24:00','19:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (37,8,'2025-08-11','18:09:00','21:40:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (38,8,'2025-08-12','18:10:00','21:21:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (39,8,'2025-08-13','12:05:11','18:41:37',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (40,8,'2025-08-14','12:08:11','18:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (41,8,'2025-08-15','18:03:00','21:47:33',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (42,8,'2025-08-17','08:20:48','18:08:43',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (43,8,'2025-08-18','18:03:00','21:42:57',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (44,8,'2025-08-19','18:09:09','21:35:08',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (45,8,'2025-08-20','18:11:00','21:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (46,8,'2025-08-21','18:15:00','21:42:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (47,8,'2025-08-22','18:09:00','21:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (48,8,'2025-08-23','14:15:00','22:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (49,8,'2025-08-25','18:10:00','21:55:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (50,8,'2025-08-26','18:12:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (51,8,'2025-08-27','18:07:00','21:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (52,8,'2025-08-28','18:00:00','21:24:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (53,8,'2025-08-30','14:10:00','21:44:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (54,8,'2025-09-01','18:00:00','21:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (55,8,'2025-09-02','18:00:00','21:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (56,8,'2025-09-03','18:00:00','21:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (57,8,'2025-09-04','18:00:00','21:53:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (58,8,'2025-09-05','17:00:00','21:35:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (59,8,'2025-09-06','18:00:00','21:56:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (60,8,'2025-09-07','09:00:00','18:37:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (61,8,'2025-09-08','18:06:00','21:46:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (62,8,'2025-09-10','18:02:00','21:32:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (63,8,'2025-09-11','18:02:00','21:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (64,8,'2025-09-12','17:59:00','21:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (65,8,'2025-09-14','08:31:00','19:45:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (66,8,'2025-09-15','18:02:00','21:23:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (67,8,'2025-09-16','18:05:00','21:27:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (68,8,'2025-09-17','18:00:00','22:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (69,8,'2025-09-18','16:58:00','21:48:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (70,8,'2025-09-19','17:53:00','22:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (71,8,'2025-09-21','08:36:00','18:54:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (72,8,'2025-09-22','17:59:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (73,8,'2025-09-24','18:03:00','21:28:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (74,8,'2025-09-25','17:55:00','21:41:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (75,8,'2025-09-26','18:03:00','21:33:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (76,8,'2025-09-28','08:10:00','20:07:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (77,8,'2025-09-29','18:06:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (78,8,'2025-09-30','18:00:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (79,8,'2025-10-01','17:57:32','21:32:19',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (80,8,'2025-10-02','18:02:25','21:16:57',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (81,10,'2025-07-01','18:00:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (82,10,'2025-07-02','18:05:00','21:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (83,10,'2025-07-03','18:00:00','21:45:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (84,10,'2025-07-04','14:00:00','22:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (85,10,'2025-07-05','08:30:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (86,10,'2025-07-07','18:02:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (87,10,'2025-07-08','18:10:00','21:40:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (88,10,'2025-07-09','18:00:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (89,10,'2025-07-10','18:05:00','21:25:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (90,10,'2025-07-11','14:10:00','21:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (91,10,'2025-07-12','08:20:00','19:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (92,10,'2025-07-14','18:00:00','21:35:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (93,10,'2025-07-15','18:08:00','21:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (94,10,'2025-07-16','18:00:00','21:48:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (95,10,'2025-07-17','18:12:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (96,10,'2025-07-18','14:05:00','21:55:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (97,10,'2025-07-19','08:25:00','18:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (98,10,'2025-07-21','18:00:00','21:40:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (99,10,'2025-07-22','18:05:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (100,10,'2025-07-23','18:10:00','21:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (101,10,'2025-07-24','18:00:00','21:25:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (102,10,'2025-07-25','14:15:00','22:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (103,10,'2025-07-26','08:15:00','19:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (104,10,'2025-07-28','18:00:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (105,10,'2025-07-29','18:08:00','21:42:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (106,10,'2025-07-30','18:00:00','21:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (107,10,'2025-07-31','18:05:00','21:38:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (108,10,'2025-08-01','14:00:00','21:45:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (109,10,'2025-08-02','08:30:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (110,10,'2025-08-04','18:00:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (111,10,'2025-08-05','18:10:00','21:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (112,10,'2025-08-06','18:00:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (113,10,'2025-08-07','18:05:00','21:35:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (114,10,'2025-08-08','14:08:00','22:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (115,10,'2025-08-09','08:20:00','19:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (116,10,'2025-08-11','18:00:00','21:25:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (117,10,'2025-08-12','18:12:00','21:48:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (118,10,'2025-08-13','18:00:00','21:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (119,10,'2025-08-14','18:05:00','21:40:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (120,10,'2025-08-15','14:10:00','21:55:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (121,10,'2025-08-16','08:25:00','18:45:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (122,10,'2025-08-18','18:00:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (123,10,'2025-08-19','18:08:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (124,10,'2025-08-20','18:00:00','21:52:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (125,10,'2025-08-21','18:10:00','21:35:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (126,10,'2025-08-22','14:00:00','22:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (127,10,'2025-08-23','08:18:00','19:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (128,10,'2025-08-25','18:00:00','21:28:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (129,10,'2025-08-26','18:05:00','21:45:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (130,10,'2025-08-27','18:00:00','21:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (131,10,'2025-08-28','18:12:00','21:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (132,10,'2025-08-29','14:05:00','21:40:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (133,10,'2025-08-30','08:22:00','18:55:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (134,10,'2025-09-01','18:00:00','21:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (135,10,'2025-09-02','18:10:00','21:35:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (136,10,'2025-09-03','18:00:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (137,10,'2025-09-04','18:05:00','21:48:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (138,10,'2025-09-05','14:08:00','22:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (139,10,'2025-09-06','08:25:00','19:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (140,10,'2025-09-08','18:00:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (141,10,'2025-09-09','18:12:00','21:42:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (142,10,'2025-09-10','18:00:00','21:25:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (143,10,'2025-09-11','18:05:00','21:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (144,10,'2025-09-12','14:00:00','21:55:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (145,10,'2025-09-13','08:30:00','18:40:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (146,10,'2025-09-15','18:00:00','21:38:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (147,10,'2025-09-16','18:08:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (148,10,'2025-09-17','18:00:00','21:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (149,10,'2025-09-18','18:10:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (150,10,'2025-09-19','14:12:00','22:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (151,10,'2025-09-20','08:20:00','19:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (152,10,'2025-09-22','18:00:00','21:25:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (153,10,'2025-09-23','18:05:00','21:40:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (154,10,'2025-09-24','18:00:00','21:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (155,10,'2025-09-25','18:12:00','21:52:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (156,10,'2025-09-26','14:05:00','21:48:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (157,10,'2025-09-27','08:28:00','18:50:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (158,10,'2025-09-29','18:00:00','21:35:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (159,10,'2025-09-30','18:10:00','21:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (160,10,'2025-10-01','18:00:00','21:45:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (161,10,'2025-10-02','18:05:00','21:30:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (162,10,'2025-10-03','18:00:00','21:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (163,10,'2025-10-04','14:10:00','21:50:00','None');
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (247,9,'2025-07-01','08:02:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (248,9,'2025-07-02','08:00:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (249,9,'2025-07-03','08:05:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (250,9,'2025-07-04','08:10:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (251,9,'2025-07-05','08:00:00','14:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (252,9,'2025-07-07','08:03:00','18:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (253,9,'2025-07-08','08:08:00','18:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (254,9,'2025-07-09','08:00:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (255,9,'2025-07-10','08:12:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (256,9,'2025-07-11','08:05:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (257,9,'2025-07-12','08:00:00','14:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (258,9,'2025-07-14','08:00:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (259,9,'2025-07-15','08:10:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (260,9,'2025-07-16','08:05:00','18:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (261,9,'2025-07-17','08:00:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (262,9,'2025-07-18','08:15:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (263,9,'2025-07-19','08:00:00','14:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (264,9,'2025-07-21','08:08:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (265,9,'2025-07-22','08:00:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (266,9,'2025-07-23','08:05:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (267,9,'2025-07-24','08:10:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (268,9,'2025-07-25','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (269,9,'2025-07-26','08:00:00','14:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (270,9,'2025-07-28','08:03:00','18:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (271,9,'2025-07-29','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (272,9,'2025-07-30','08:12:00','18:25:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (273,9,'2025-07-31','08:05:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (274,9,'2025-08-01','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (275,9,'2025-08-02','08:00:00','14:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (276,9,'2025-08-04','08:10:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (277,9,'2025-08-05','08:05:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (278,9,'2025-08-06','08:00:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (279,9,'2025-08-07','08:08:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (280,9,'2025-08-08','08:00:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (281,9,'2025-08-09','08:00:00','14:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (282,9,'2025-08-11','08:12:00','18:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (283,9,'2025-08-12','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (284,9,'2025-08-13','08:05:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (285,9,'2025-08-14','08:10:00','18:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (286,9,'2025-08-15','08:00:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (287,9,'2025-08-16','08:00:00','14:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (288,9,'2025-08-18','08:08:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (289,9,'2025-08-19','08:00:00','18:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (290,9,'2025-08-20','08:15:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (291,9,'2025-08-21','08:05:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (292,9,'2025-08-22','08:00:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (293,9,'2025-08-23','08:00:00','14:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (294,9,'2025-08-25','08:10:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (295,9,'2025-08-26','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (296,9,'2025-08-27','08:05:00','18:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (297,9,'2025-08-28','08:00:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (298,9,'2025-08-29','08:12:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (299,9,'2025-08-30','08:00:00','14:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (300,9,'2025-09-01','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (301,9,'2025-09-02','08:08:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (302,9,'2025-09-03','08:00:00','18:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (303,9,'2025-09-04','08:05:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (304,9,'2025-09-05','08:10:00','18:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (305,9,'2025-09-06','08:00:00','14:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (306,9,'2025-09-08','08:00:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (307,9,'2025-09-09','08:12:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (308,9,'2025-09-10','08:05:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (309,9,'2025-09-11','08:00:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (310,9,'2025-09-12','08:08:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (311,9,'2025-09-13','08:00:00','14:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (312,9,'2025-09-15','08:10:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (313,9,'2025-09-16','08:00:00','18:18:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (314,9,'2025-09-17','08:05:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (315,9,'2025-09-18','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (316,9,'2025-09-19','08:15:00','18:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (317,9,'2025-09-20','08:00:00','14:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (318,9,'2025-09-22','08:00:00','18:08:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (319,9,'2025-09-23','08:10:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (320,9,'2025-09-24','08:05:00','18:20:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (321,9,'2025-09-25','08:00:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (322,9,'2025-09-26','08:08:00','18:05:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (323,9,'2025-09-27','08:00:00','14:12:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (324,9,'2025-09-29','08:00:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (325,9,'2025-09-30','08:12:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (326,9,'2025-10-01','08:00:00','18:10:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (327,9,'2025-10-02','08:05:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (328,9,'2025-10-03','08:10:00','18:15:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (329,9,'2025-10-04','08:00:00','14:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (553,7,'2025-10-01','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (554,9,'2025-10-09','08:00:00','18:00:00',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (555,8,'2025-10-04','14:06:30','21:28:43',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (556,8,'2025-10-05','08:25:46','19:13:49',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (557,8,'2025-10-06','18:02:11','21:18:06',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (558,8,'2025-10-07','17:41:15','21:41:42',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (559,8,'2025-10-08','18:04:12','21:30:40',NULL);
INSERT INTO `records` (`id`, `user_id`, `data`, `hora_entrada`, `hora_saida`, `observacoes`) VALUES (560,8,'2025-10-09','17:42:33','21:27:38',NULL);
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `solicitacoes_correcao`
--

LOCK TABLES `solicitacoes_correcao` WRITE;
/*!40000 ALTER TABLE `solicitacoes_correcao` DISABLE KEYS */;
INSERT INTO `solicitacoes_correcao` (`id`, `funcionaria_id`, `data_solicitacao`, `data_registro`, `tipo`, `horario_entrada`, `horario_saida`, `justificativa`, `status`, `observacao_admin`, `data_processamento`) VALUES (1,9,'2025-10-04 14:32:47','2025-10-04','saida',NULL,'14:00:00','Ajuste','aprovado','Aprovado','2025-10-04 14:34:17');
INSERT INTO `solicitacoes_correcao` (`id`, `funcionaria_id`, `data_solicitacao`, `data_registro`, `tipo`, `horario_entrada`, `horario_saida`, `justificativa`, `status`, `observacao_admin`, `data_processamento`) VALUES (2,7,'2025-10-08 23:49:25','2025-10-01','ambos','08:00:00','18:00:00','Esqueci','aprovado','Aprovado','2025-10-08 23:51:50');
INSERT INTO `solicitacoes_correcao` (`id`, `funcionaria_id`, `data_solicitacao`, `data_registro`, `tipo`, `horario_entrada`, `horario_saida`, `justificativa`, `status`, `observacao_admin`, `data_processamento`) VALUES (3,9,'2025-10-10 11:38:06','2025-10-09','ambos','08:00:00','18:00:00','Esqueci','aprovado','Aprovado em lote','2025-10-10 11:38:58');
/*!40000 ALTER TABLE `solicitacoes_correcao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `configuracoes_pagamento`
--

LOCK TABLES `configuracoes_pagamento` WRITE;
/*!40000 ALTER TABLE `configuracoes_pagamento` DISABLE KEYS */;
INSERT INTO `configuracoes_pagamento` (`id`, `tipo_dia`, `valor_hora`, `data_criacao`, `data_atualizacao`, `atualizado_por`, `ativo`) VALUES (1,'segunda',6.90,'2025-10-06 20:36:09','2025-10-06 20:36:09','Sistema - Valor Inicial',1);
INSERT INTO `configuracoes_pagamento` (`id`, `tipo_dia`, `valor_hora`, `data_criacao`, `data_atualizacao`, `atualizado_por`, `ativo`) VALUES (2,'terca',6.90,'2025-10-06 20:36:09','2025-10-06 20:36:09','Sistema - Valor Inicial',1);
INSERT INTO `configuracoes_pagamento` (`id`, `tipo_dia`, `valor_hora`, `data_criacao`, `data_atualizacao`, `atualizado_por`, `ativo`) VALUES (3,'quarta',6.90,'2025-10-06 20:36:09','2025-10-06 20:36:09','Sistema - Valor Inicial',1);
INSERT INTO `configuracoes_pagamento` (`id`, `tipo_dia`, `valor_hora`, `data_criacao`, `data_atualizacao`, `atualizado_por`, `ativo`) VALUES (4,'quinta',6.90,'2025-10-06 20:36:09','2025-10-06 20:36:09','Sistema - Valor Inicial',1);
INSERT INTO `configuracoes_pagamento` (`id`, `tipo_dia`, `valor_hora`, `data_criacao`, `data_atualizacao`, `atualizado_por`, `ativo`) VALUES (5,'sexta',6.90,'2025-10-06 20:36:09','2025-10-06 20:36:09','Sistema - Valor Inicial',1);
INSERT INTO `configuracoes_pagamento` (`id`, `tipo_dia`, `valor_hora`, `data_criacao`, `data_atualizacao`, `atualizado_por`, `ativo`) VALUES (6,'sabado',6.90,'2025-10-06 20:36:09','2025-10-06 20:36:09','Sistema - Valor Inicial',1);
INSERT INTO `configuracoes_pagamento` (`id`, `tipo_dia`, `valor_hora`, `data_criacao`, `data_atualizacao`, `atualizado_por`, `ativo`) VALUES (7,'domingo',10.00,'2025-10-06 20:36:09','2025-10-06 20:36:09','Sistema - Valor Inicial',1);
/*!40000 ALTER TABLE `configuracoes_pagamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `historico_alteracoes`
--

LOCK TABLES `historico_alteracoes` WRITE;
/*!40000 ALTER TABLE `historico_alteracoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `historico_alteracoes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-10 18:04:22
