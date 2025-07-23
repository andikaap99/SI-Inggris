-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 22, 2025 at 04:06 PM
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('d44e47d7782d');

-- --------------------------------------------------------

--
-- Table structure for table `Attempt_Complete_Sentence`
--

CREATE TABLE `Attempt_Complete_Sentence` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Attempt_Complete_Sentence`
--

INSERT INTO `Attempt_Complete_Sentence` (`Id_attempt`, `score`, `attempted_at`, `user_id`, `Id_cat`) VALUES
(1, 100, '2025-07-20 23:21:24', 1, 1),
(2, 100, '2025-07-20 23:03:47', 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `Attempt_Complete_Sentences`
--

CREATE TABLE `Attempt_Complete_Sentences` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Attempt_Image_Word`
--

CREATE TABLE `Attempt_Image_Word` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Attempt_Image_Word`
--

INSERT INTO `Attempt_Image_Word` (`Id_attempt`, `score`, `attempted_at`, `user_id`, `Id_cat`) VALUES
(1, 100, '2025-07-22 09:50:42', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Attempt_Listening_Sentence`
--

CREATE TABLE `Attempt_Listening_Sentence` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Attempt_Listening_Word`
--

CREATE TABLE `Attempt_Listening_Word` (
  `Id_attempt` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Attempt_Listening_Word`
--

INSERT INTO `Attempt_Listening_Word` (`Id_attempt`, `score`, `attempted_at`, `user_id`, `Id_cat`) VALUES
(1, 100, '2025-07-21 05:31:24', 1, 1),
(3, 0, '2025-07-22 09:50:19', 1, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Category`
--

CREATE TABLE `Category` (
  `Id_cat` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `desc` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Category`
--

INSERT INTO `Category` (`Id_cat`, `name`, `desc`) VALUES
(1, 'Past Tense', 'All about past tense here mate!'),
(2, 'Future Tense', 'Let\'s talk about our future!'),
(3, 'Animal', 'Miaw-Miaw Woof-Woof Auuuu! ');

-- --------------------------------------------------------

--
-- Table structure for table `Complete_Sentence`
--

CREATE TABLE `Complete_Sentence` (
  `Id_cs` int(11) NOT NULL,
  `question_cs` varchar(255) DEFAULT NULL,
  `cs_answer` varchar(255) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Complete_Sentence`
--

INSERT INTO `Complete_Sentence` (`Id_cs`, `question_cs`, `cs_answer`, `Id_cat`) VALUES
(1, 'Yesterday I ___ to my girlfirend house', 'went', 1),
(2, 'I ___ buy a Computer next week', 'will', 2);

-- --------------------------------------------------------

--
-- Table structure for table `Global_Attempt`
--

CREATE TABLE `Global_Attempt` (
  `id` int(11) NOT NULL,
  `score` float DEFAULT NULL,
  `attempted_at` datetime DEFAULT current_timestamp(),
  `feature_type` varchar(50) NOT NULL,
  `Id_cat` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Global_Attempt`
--

INSERT INTO `Global_Attempt` (`id`, `score`, `attempted_at`, `feature_type`, `Id_cat`, `user_id`) VALUES
(4, 100, '2025-07-20 23:21:24', 'Complete_Sentence', 1, 1),
(5, 100, '2025-07-21 06:03:47', 'Complete_Sentence', 2, 1),
(6, 100, '2025-07-22 09:50:42', 'Image_Word', 3, 1),
(7, 0, '2025-07-22 09:50:19', 'Listening_Word', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `Image_Word`
--

CREATE TABLE `Image_Word` (
  `Id_iw` int(11) NOT NULL,
  `iw_answer` varchar(30) DEFAULT NULL,
  `image_iw` varchar(255) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Image_Word`
--

INSERT INTO `Image_Word` (`Id_iw`, `iw_answer`, `image_iw`, `Id_cat`) VALUES
(1, 'cat', 'https://github.com/andikaap99/asset/blob/main/kucing.jpeg?raw=true', 3);

-- --------------------------------------------------------

--
-- Table structure for table `Keyword_Listening`
--

CREATE TABLE `Keyword_Listening` (
  `Id_keyword` int(11) NOT NULL,
  `keyword_answer` varchar(30) DEFAULT NULL,
  `Id_ls` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Listening_Sentence`
--

CREATE TABLE `Listening_Sentence` (
  `Id_ls` int(11) NOT NULL,
  `sentence_ls` varchar(100) DEFAULT NULL,
  `audio_ls` varchar(255) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Listening_Word`
--

CREATE TABLE `Listening_Word` (
  `Id_lw` int(11) NOT NULL,
  `lw_answer` varchar(30) DEFAULT NULL,
  `audio_lw` varchar(255) DEFAULT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Listening_Word`
--

INSERT INTO `Listening_Word` (`Id_lw`, `lw_answer`, `audio_lw`, `Id_cat`) VALUES
(1, 'cat', 'https://raw.githubusercontent.com/andikaap99/asset/main/Hello! Sound Effect.mp3', 3);

-- --------------------------------------------------------

--
-- Table structure for table `Materi`
--

CREATE TABLE `Materi` (
  `Id_mat` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `url` varchar(255) NOT NULL,
  `Id_cat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Materi`
--

INSERT INTO `Materi` (`Id_mat`, `name`, `url`, `Id_cat`) VALUES
(2, 'kimins', 'https://drive.google.com/file/d/1blsEf2RU1jXoTnKQrZKeMta6K8Unn0Wx/view?usp=sharing', 1),
(3, 'How to Learn Past Tense Fast No Root', 'https://drive.google.com/file/d/1blsEf2RU1jXoTnKQrZKeMta6K8Unn0Wx/view?usp=sharing', 3),
(5, 'beji', 'https://drive.google.com/file/d/1blsEf2RU1jXoTnKQrZKeMta6K8Unn0Wx/view?usp=sharing', 2);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `class_name` varchar(10) DEFAULT NULL,
  `total_score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `user_id`, `name`, `class_name`, `total_score`) VALUES
(1, 1, 'Andika Aryadi Putra', 'IPA 2', 300);

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `total_score` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `hashed_password`, `role`, `name`, `total_score`) VALUES
(1, 'andika-teacher', '$2b$12$V1xldoYW4fukjRgIOUHibOXlzn7u62yFOAOQFl5XUtAdoJIedyek6', 'student', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `Attempt_Complete_Sentence`
--
ALTER TABLE `Attempt_Complete_Sentence`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Attempt_Complete_Sentences`
--
ALTER TABLE `Attempt_Complete_Sentences`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Attempt_Image_Word`
--
ALTER TABLE `Attempt_Image_Word`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Attempt_Listening_Sentence`
--
ALTER TABLE `Attempt_Listening_Sentence`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Attempt_Listening_Word`
--
ALTER TABLE `Attempt_Listening_Word`
  ADD PRIMARY KEY (`Id_attempt`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Category`
--
ALTER TABLE `Category`
  ADD PRIMARY KEY (`Id_cat`),
  ADD KEY `ix_Category_Id_cat` (`Id_cat`);

--
-- Indexes for table `Complete_Sentence`
--
ALTER TABLE `Complete_Sentence`
  ADD PRIMARY KEY (`Id_cs`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Global_Attempt`
--
ALTER TABLE `Global_Attempt`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `Image_Word`
--
ALTER TABLE `Image_Word`
  ADD PRIMARY KEY (`Id_iw`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Keyword_Listening`
--
ALTER TABLE `Keyword_Listening`
  ADD PRIMARY KEY (`Id_keyword`),
  ADD KEY `Id_ls` (`Id_ls`);

--
-- Indexes for table `Listening_Sentence`
--
ALTER TABLE `Listening_Sentence`
  ADD PRIMARY KEY (`Id_ls`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Listening_Word`
--
ALTER TABLE `Listening_Word`
  ADD PRIMARY KEY (`Id_lw`),
  ADD KEY `Id_cat` (`Id_cat`);

--
-- Indexes for table `Materi`
--
ALTER TABLE `Materi`
  ADD PRIMARY KEY (`Id_mat`),
  ADD KEY `Id_cat` (`Id_cat`),
  ADD KEY `ix_Materi_Id_mat` (`Id_mat`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Attempt_Complete_Sentence`
--
ALTER TABLE `Attempt_Complete_Sentence`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Attempt_Complete_Sentences`
--
ALTER TABLE `Attempt_Complete_Sentences`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Attempt_Image_Word`
--
ALTER TABLE `Attempt_Image_Word`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `Attempt_Listening_Sentence`
--
ALTER TABLE `Attempt_Listening_Sentence`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Attempt_Listening_Word`
--
ALTER TABLE `Attempt_Listening_Word`
  MODIFY `Id_attempt` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Category`
--
ALTER TABLE `Category`
  MODIFY `Id_cat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Complete_Sentence`
--
ALTER TABLE `Complete_Sentence`
  MODIFY `Id_cs` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Global_Attempt`
--
ALTER TABLE `Global_Attempt`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `Image_Word`
--
ALTER TABLE `Image_Word`
  MODIFY `Id_iw` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Keyword_Listening`
--
ALTER TABLE `Keyword_Listening`
  MODIFY `Id_keyword` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Listening_Sentence`
--
ALTER TABLE `Listening_Sentence`
  MODIFY `Id_ls` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Listening_Word`
--
ALTER TABLE `Listening_Word`
  MODIFY `Id_lw` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `Materi`
--
ALTER TABLE `Materi`
  MODIFY `Id_mat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Attempt_Complete_Sentence`
--
ALTER TABLE `Attempt_Complete_Sentence`
  ADD CONSTRAINT `Attempt_Complete_Sentence_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `Attempt_Complete_Sentence_ibfk_2` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Attempt_Complete_Sentences`
--
ALTER TABLE `Attempt_Complete_Sentences`
  ADD CONSTRAINT `Attempt_Complete_Sentences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `Attempt_Complete_Sentences_ibfk_2` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Attempt_Image_Word`
--
ALTER TABLE `Attempt_Image_Word`
  ADD CONSTRAINT `Attempt_Image_Word_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `Attempt_Image_Word_ibfk_2` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Attempt_Listening_Sentence`
--
ALTER TABLE `Attempt_Listening_Sentence`
  ADD CONSTRAINT `Attempt_Listening_Sentence_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `Attempt_Listening_Sentence_ibfk_2` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Attempt_Listening_Word`
--
ALTER TABLE `Attempt_Listening_Word`
  ADD CONSTRAINT `Attempt_Listening_Word_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `Attempt_Listening_Word_ibfk_2` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Complete_Sentence`
--
ALTER TABLE `Complete_Sentence`
  ADD CONSTRAINT `Complete_Sentence_ibfk_1` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Global_Attempt`
--
ALTER TABLE `Global_Attempt`
  ADD CONSTRAINT `Global_Attempt_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `Image_Word`
--
ALTER TABLE `Image_Word`
  ADD CONSTRAINT `Image_Word_ibfk_1` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Keyword_Listening`
--
ALTER TABLE `Keyword_Listening`
  ADD CONSTRAINT `Keyword_Listening_ibfk_1` FOREIGN KEY (`Id_ls`) REFERENCES `Listening_Sentence` (`Id_ls`);

--
-- Constraints for table `Listening_Sentence`
--
ALTER TABLE `Listening_Sentence`
  ADD CONSTRAINT `Listening_Sentence_ibfk_1` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Listening_Word`
--
ALTER TABLE `Listening_Word`
  ADD CONSTRAINT `Listening_Word_ibfk_1` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `Materi`
--
ALTER TABLE `Materi`
  ADD CONSTRAINT `Materi_ibfk_1` FOREIGN KEY (`Id_cat`) REFERENCES `Category` (`Id_cat`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `teachers`
--
ALTER TABLE `teachers`
  ADD CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
