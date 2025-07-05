-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 05, 2025 at 07:05 PM
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
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('d44e47d7782d');

-- --------------------------------------------------------

--
-- Table structure for table `attempt_complete_sentences`
--

CREATE TABLE `attempt_complete_sentences` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_category` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `attempt_complete_sentences`
--

INSERT INTO `attempt_complete_sentences` (`Id_attempt`, `score`, `attempted_at`, `user_id`, `Id_category`) VALUES
(7, 100, '2025-07-05 15:54:01', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `attempt_image_word`
--

CREATE TABLE `attempt_image_word` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_category` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `attempt_image_word`
--

INSERT INTO `attempt_image_word` (`Id_attempt`, `score`, `attempted_at`, `user_id`, `Id_category`) VALUES
(5, 100, '2025-07-05 14:55:53', 3, 1),
(7, 0, '2025-07-05 15:52:35', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `attempt_listening_sentence`
--

CREATE TABLE `attempt_listening_sentence` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_category` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attempt_listening_word`
--

CREATE TABLE `attempt_listening_word` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_category` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `attempt_listening_word`
--

INSERT INTO `attempt_listening_word` (`Id_attempt`, `score`, `attempted_at`, `user_id`, `Id_category`) VALUES
(5, 100, '2025-07-05 22:07:47', 6, 1),
(8, 100, '2025-07-05 15:51:40', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `category_complete_sentence`
--

CREATE TABLE `category_complete_sentence` (
  `Id_ccs` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `category_complete_sentence`
--

INSERT INTO `category_complete_sentence` (`Id_ccs`, `name`) VALUES
(1, 'Daily Object');

-- --------------------------------------------------------

--
-- Table structure for table `category_image_word`
--

CREATE TABLE `category_image_word` (
  `Id_ciw` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `category_image_word`
--

INSERT INTO `category_image_word` (`Id_ciw`, `name`) VALUES
(1, 'Daily Object');

-- --------------------------------------------------------

--
-- Table structure for table `category_listening_sentence`
--

CREATE TABLE `category_listening_sentence` (
  `Id_cls` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `category_listening_sentence`
--

INSERT INTO `category_listening_sentence` (`Id_cls`, `name`) VALUES
(1, 'Daily Object');

-- --------------------------------------------------------

--
-- Table structure for table `category_listening_word`
--

CREATE TABLE `category_listening_word` (
  `Id_clw` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `category_listening_word`
--

INSERT INTO `category_listening_word` (`Id_clw`, `name`) VALUES
(1, 'Daily Object');

-- --------------------------------------------------------

--
-- Table structure for table `complete_sentence`
--

CREATE TABLE `complete_sentence` (
  `Id_cs` int(11) NOT NULL,
  `question_cs` varchar(255) DEFAULT NULL,
  `cs_answer` varchar(255) DEFAULT NULL,
  `Id_ccs` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `complete_sentence`
--

INSERT INTO `complete_sentence` (`Id_cs`, `question_cs`, `cs_answer`, `Id_ccs`) VALUES
(1, 'Yesterday I ___ to the park', 'Went', 1),
(2, 'what ___ you doing?', 'are', 1);

-- --------------------------------------------------------

--
-- Table structure for table `global_attempt`
--

CREATE TABLE `global_attempt` (
  `id` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `feature_type` varchar(50) NOT NULL,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `global_attempt`
--

INSERT INTO `global_attempt` (`id`, `score`, `attempted_at`, `feature_type`, `category_id`, `user_id`) VALUES
(8, 100, '2025-07-05 14:55:53', 'Image_Word', 1, 3),
(9, 100, '2025-07-05 22:07:47', 'Listening_Word', 1, 6),
(16, 100, '2025-07-05 15:51:40', 'Listening_Word', 1, 1),
(17, 0, '2025-07-05 15:52:35', 'Image_Word', 1, 1),
(18, 100, '2025-07-05 15:54:01', 'Complete_Sentences', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `image_word`
--

CREATE TABLE `image_word` (
  `Id_iw` int(11) NOT NULL,
  `iw_answer` varchar(30) DEFAULT NULL,
  `image_iw` varchar(255) DEFAULT NULL,
  `Id_ciw` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `image_word`
--

INSERT INTO `image_word` (`Id_iw`, `iw_answer`, `image_iw`, `Id_ciw`) VALUES
(1, 'cat', 'https://github.com/andikaap99/asset/blob/main/kucing.jpeg?raw=true', 1);

-- --------------------------------------------------------

--
-- Table structure for table `keyword_listening`
--

CREATE TABLE `keyword_listening` (
  `Id_keyword` int(11) NOT NULL,
  `keyword_answer` varchar(30) DEFAULT NULL,
  `Id_ls` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `listening_sentence`
--

CREATE TABLE `listening_sentence` (
  `Id_ls` int(11) NOT NULL,
  `sentence_ls` varchar(100) DEFAULT NULL,
  `audio_ls` varchar(255) DEFAULT NULL,
  `Id_cls` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `listening_sentence`
--

INSERT INTO `listening_sentence` (`Id_ls`, `sentence_ls`, `audio_ls`, `Id_cls`) VALUES
(1, 'hello', 'https://raw.githubusercontent.com/andikaap99/asset/main/Hello! Sound Effect.mp3', 1);

-- --------------------------------------------------------

--
-- Table structure for table `listening_word`
--

CREATE TABLE `listening_word` (
  `Id_lw` int(11) NOT NULL,
  `lw_answer` varchar(30) DEFAULT NULL,
  `audio_lw` varchar(255) DEFAULT NULL,
  `Id_clw` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `listening_word`
--

INSERT INTO `listening_word` (`Id_lw`, `lw_answer`, `audio_lw`, `Id_clw`) VALUES
(1, 'hello', 'https://raw.githubusercontent.com/andikaap99/asset/main/Hello! Sound Effect.mp3', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nis` varchar(20) DEFAULT NULL,
  `hashed_password` varchar(255) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `total_score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nis`, `hashed_password`, `role`, `name`, `total_score`) VALUES
(1, '10123196', '$2b$12$NC7IWn180HEix1ZQsXGOtuo2DzzmqTJ2rzyzU97IEWOpevces0WYW', 'admin', 'Andika Aryadi Putra', 200),
(2, '10123177', '$2b$12$NC7IWn180HEix1ZQsXGOtuo2DzzmqTJ2rzyzU97IEWOpevces0WYW', 'admin', ' Mutiara Annur', 0),
(3, '10123195', '$2b$12$NC7IWn180HEix1ZQsXGOtuo2DzzmqTJ2rzyzU97IEWOpevces0WYW', 'admin', 'Ardi Saputra', 100),
(4, '10123193', '$2b$12$NC7IWn180HEix1ZQsXGOtuo2DzzmqTJ2rzyzU97IEWOpevces0WYW', 'admin', 'Annisa Nuraeni', 0),
(5, '10123197', '$2b$12$NC7IWn180HEix1ZQsXGOtuo2DzzmqTJ2rzyzU97IEWOpevces0WYW', 'admin', 'Topik Nur Rahman', 0),
(6, '10123212', '$2b$12$NC7IWn180HEix1ZQsXGOtuo2DzzmqTJ2rzyzU97IEWOpevces0WYW', 'admin', 'Rizza Alyda Yahya', 100);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `attempt_complete_sentences`
--
ALTER TABLE `attempt_complete_sentences`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_category` (`Id_category`);

--
-- Indexes for table `attempt_image_word`
--
ALTER TABLE `attempt_image_word`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_category` (`Id_category`);

--
-- Indexes for table `attempt_listening_sentence`
--
ALTER TABLE `attempt_listening_sentence`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_category` (`Id_category`);

--
-- Indexes for table `attempt_listening_word`
--
ALTER TABLE `attempt_listening_word`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_category` (`Id_category`);

--
-- Indexes for table `category_complete_sentence`
--
ALTER TABLE `category_complete_sentence`
  ADD PRIMARY KEY (`Id_ccs`);

--
-- Indexes for table `category_image_word`
--
ALTER TABLE `category_image_word`
  ADD PRIMARY KEY (`Id_ciw`);

--
-- Indexes for table `category_listening_sentence`
--
ALTER TABLE `category_listening_sentence`
  ADD PRIMARY KEY (`Id_cls`);

--
-- Indexes for table `category_listening_word`
--
ALTER TABLE `category_listening_word`
  ADD PRIMARY KEY (`Id_clw`);

--
-- Indexes for table `complete_sentence`
--
ALTER TABLE `complete_sentence`
  ADD PRIMARY KEY (`Id_cs`),
  ADD KEY `Id_ccs` (`Id_ccs`);

--
-- Indexes for table `global_attempt`
--
ALTER TABLE `global_attempt`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `image_word`
--
ALTER TABLE `image_word`
  ADD PRIMARY KEY (`Id_iw`),
  ADD KEY `Id_ciw` (`Id_ciw`);

--
-- Indexes for table `keyword_listening`
--
ALTER TABLE `keyword_listening`
  ADD PRIMARY KEY (`Id_keyword`),
  ADD KEY `Id_ls` (`Id_ls`);

--
-- Indexes for table `listening_sentence`
--
ALTER TABLE `listening_sentence`
  ADD PRIMARY KEY (`Id_ls`),
  ADD KEY `Id_cls` (`Id_cls`);

--
-- Indexes for table `listening_word`
--
ALTER TABLE `listening_word`
  ADD PRIMARY KEY (`Id_lw`),
  ADD KEY `Id_clw` (`Id_clw`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_nis` (`nis`),
  ADD KEY `ix_users_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attempt_complete_sentences`
--
ALTER TABLE `attempt_complete_sentences`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `attempt_image_word`
--
ALTER TABLE `attempt_image_word`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `attempt_listening_sentence`
--
ALTER TABLE `attempt_listening_sentence`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attempt_listening_word`
--
ALTER TABLE `attempt_listening_word`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `category_complete_sentence`
--
ALTER TABLE `category_complete_sentence`
  MODIFY `Id_ccs` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `category_image_word`
--
ALTER TABLE `category_image_word`
  MODIFY `Id_ciw` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `category_listening_sentence`
--
ALTER TABLE `category_listening_sentence`
  MODIFY `Id_cls` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `category_listening_word`
--
ALTER TABLE `category_listening_word`
  MODIFY `Id_clw` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `complete_sentence`
--
ALTER TABLE `complete_sentence`
  MODIFY `Id_cs` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `global_attempt`
--
ALTER TABLE `global_attempt`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `image_word`
--
ALTER TABLE `image_word`
  MODIFY `Id_iw` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `keyword_listening`
--
ALTER TABLE `keyword_listening`
  MODIFY `Id_keyword` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `listening_sentence`
--
ALTER TABLE `listening_sentence`
  MODIFY `Id_ls` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `listening_word`
--
ALTER TABLE `listening_word`
  MODIFY `Id_lw` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attempt_complete_sentences`
--
ALTER TABLE `attempt_complete_sentences`
  ADD CONSTRAINT `attempt_complete_sentences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `attempt_complete_sentences_ibfk_2` FOREIGN KEY (`Id_category`) REFERENCES `category_complete_sentence` (`Id_ccs`);

--
-- Constraints for table `attempt_image_word`
--
ALTER TABLE `attempt_image_word`
  ADD CONSTRAINT `attempt_image_word_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `attempt_image_word_ibfk_2` FOREIGN KEY (`Id_category`) REFERENCES `category_image_word` (`Id_ciw`);

--
-- Constraints for table `attempt_listening_sentence`
--
ALTER TABLE `attempt_listening_sentence`
  ADD CONSTRAINT `attempt_listening_sentence_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `attempt_listening_sentence_ibfk_2` FOREIGN KEY (`Id_category`) REFERENCES `category_listening_sentence` (`Id_cls`);

--
-- Constraints for table `attempt_listening_word`
--
ALTER TABLE `attempt_listening_word`
  ADD CONSTRAINT `attempt_listening_word_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `attempt_listening_word_ibfk_2` FOREIGN KEY (`Id_category`) REFERENCES `category_listening_word` (`Id_clw`);

--
-- Constraints for table `complete_sentence`
--
ALTER TABLE `complete_sentence`
  ADD CONSTRAINT `complete_sentence_ibfk_1` FOREIGN KEY (`Id_ccs`) REFERENCES `category_complete_sentence` (`Id_ccs`);

--
-- Constraints for table `global_attempt`
--
ALTER TABLE `global_attempt`
  ADD CONSTRAINT `global_attempt_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `image_word`
--
ALTER TABLE `image_word`
  ADD CONSTRAINT `image_word_ibfk_1` FOREIGN KEY (`Id_ciw`) REFERENCES `category_image_word` (`Id_ciw`);

--
-- Constraints for table `keyword_listening`
--
ALTER TABLE `keyword_listening`
  ADD CONSTRAINT `keyword_listening_ibfk_1` FOREIGN KEY (`Id_ls`) REFERENCES `listening_sentence` (`Id_ls`);

--
-- Constraints for table `listening_sentence`
--
ALTER TABLE `listening_sentence`
  ADD CONSTRAINT `listening_sentence_ibfk_1` FOREIGN KEY (`Id_cls`) REFERENCES `category_listening_sentence` (`Id_cls`);

--
-- Constraints for table `listening_word`
--
ALTER TABLE `listening_word`
  ADD CONSTRAINT `listening_word_ibfk_1` FOREIGN KEY (`Id_clw`) REFERENCES `category_listening_word` (`Id_clw`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
