-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 26, 2025 at 03:40 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `image_word`
--

CREATE TABLE `image_word` (
  `Id_iw` int(11) NOT NULL,
  `iw_answer` varchar(30) DEFAULT NULL,
  `image_iw` varchar(400) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `image_word`
--

INSERT INTO `image_word` (`Id_iw`, `iw_answer`, `image_iw`) VALUES
(1, 'glass', 'https://github.com/andikaap99/asset/blob/main/glass.jpg?raw=true'),
(2, 'cat', 'https://github.com/andikaap99/asset/blob/main/kucing.jpeg?raw=true'),
(3, 'woman', 'https://github.com/andikaap99/asset/blob/main/sullyoon.jpg?raw=true');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `image_word`
--
ALTER TABLE `image_word`
  ADD PRIMARY KEY (`Id_iw`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `image_word`
--
ALTER TABLE `image_word`
  MODIFY `Id_iw` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
