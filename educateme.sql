-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 01, 2023 at 05:34 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `educateme`
--

-- --------------------------------------------------------

--
-- Table structure for table `coursepages`
--

CREATE TABLE `coursepages` (
  `course_id` int(11) NOT NULL,
  `page_name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `coursepages`
--

INSERT INTO `coursepages` (`course_id`, `page_name`) VALUES
(23, 'introduction');

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `course_name` varchar(100) NOT NULL,
  `course_id` int(11) NOT NULL,
  `course_pages` int(11) DEFAULT 1,
  `students_enrolled` int(11) DEFAULT 0,
  `editor_id` int(11) DEFAULT NULL,
  `course_intro` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`course_name`, `course_id`, `course_pages`, `students_enrolled`, `editor_id`, `course_intro`) VALUES
('Artificial Intelligence', 1, 11, 7, 1, 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Sequi cum mollitia deserunt debitis autem nobis             dignissimos non blanditiis harum accusamus explicabo accusantium commodi earum labo'),
('Web Engineering', 4, 10, 9, 1, 'Ladipisicing elit. Sequi cum mollitia deserunt debitis autem nobis             dignissimos non blanditiis harum'),
('Compiler Construction', 7, 10, 6, 1, '\"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut '),
('Computer Networks', 9, 10, 0, 1, 'df ref fhkdj'),
('CSS5', 13, 0, 0, 4, 'this is a css5 course. It stands for cascaded style sheets.'),
('Basic Electronics', 15, 0, 0, 4, 'this is a basic electronics course. It includes circuits,laws,current etc'),
('EMT', 18, 0, 0, 4, 'Consectetur adipisicing elit. Sequi cum mollitia deserunt debitis autem nobis             dig'),
('JavaScript', 19, 0, 0, 4, 'THIS IS JS COURSE'),
('CC', 20, 0, 0, 4, 'THIS IS CC COURSE'),
('Python', 23, 1, 0, 1, 'this is python course');

-- --------------------------------------------------------

--
-- Table structure for table `editors`
--

CREATE TABLE `editors` (
  `editor_name` varchar(20) NOT NULL,
  `editor_id` int(11) NOT NULL,
  `editor_email` varchar(20) NOT NULL,
  `editor_password` varchar(20) NOT NULL,
  `editor_contact` varchar(20) DEFAULT NULL,
  `editor_courses` int(11) DEFAULT 0,
  `editor_picture` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `editors`
--

INSERT INTO `editors` (`editor_name`, `editor_id`, `editor_email`, `editor_password`, `editor_contact`, `editor_courses`, `editor_picture`) VALUES
('Arsal', 1, 'arsal789@gmail.com', 'arsal789', '03125679234', 5, 'arsal.png'),
('Laiba Tariq', 4, 'laiba462@gmail.com', 'laiba462', '03134270581', 5, 'profile3_1.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

CREATE TABLE `enrollment` (
  `user_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `enrollment_id` int(11) NOT NULL,
  `pages_read` int(11) DEFAULT NULL,
  `progress` varchar(5) DEFAULT '0%'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` (`user_id`, `course_id`, `enrollment_id`, `pages_read`, `progress`) VALUES
(6, 1, 1, 0, '0%'),
(6, 4, 2, 0, '0%'),
(13, 1, 6, 0, '0%'),
(13, 4, 7, 0, '0%'),
(13, 7, 9, 0, '0%'),
(1, 7, 10, 0, '0%'),
(12, 1, 11, 0, '0%'),
(1, 4, 12, 0, '0%'),
(1, 23, 13, 0, '0%'),
(1, 1, 14, 0, '0%');

-- --------------------------------------------------------

--
-- Table structure for table `quizzes`
--

CREATE TABLE `quizzes` (
  `question_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `question` varchar(255) NOT NULL,
  `option1` varchar(100) NOT NULL,
  `option2` varchar(100) NOT NULL,
  `option3` varchar(100) NOT NULL,
  `option4` varchar(100) NOT NULL,
  `correct_answer` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `suggestions`
--

CREATE TABLE `suggestions` (
  `suggestion_id` int(11) NOT NULL,
  `suggestion_date` date DEFAULT NULL,
  `suggestion_text` varchar(100) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `suggestions`
--

INSERT INTO `suggestions` (`suggestion_id`, `suggestion_date`, `suggestion_text`, `user_id`) VALUES
(1, '2022-07-14', 'Well explained... need to update example sections of HTML', 1),
(2, '2022-07-30', 'cus fwd wef\'fv ', 13);

-- --------------------------------------------------------

--
-- Table structure for table `useranswers`
--

CREATE TABLE `useranswers` (
  `user_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `user_answer` varchar(45) DEFAULT NULL,
  `answer_status` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `userprogress`
--

CREATE TABLE `userprogress` (
  `sr_no` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `page_name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_name` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(20) NOT NULL,
  `user_courses` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_name`, `user_id`, `user_email`, `user_password`, `user_courses`) VALUES
('Laiba', 1, 'laiba@gmail.com', 'laiba1234', 2),
('usama', 6, 'usama@gmail.com', 'usama123', 0),
('Laiba Tariq', 11, 'laiba033545@gmail.co', 'laiba980', 0),
('Syeda Laiba', 12, 'laiba033545@gmail.com', 'laiba980', 1),
('Laiba Tariq', 13, 'laibatariq461@gmail.com', 'laiba461', 7);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `coursepages`
--
ALTER TABLE `coursepages`
  ADD PRIMARY KEY (`course_id`,`page_name`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`course_id`),
  ADD KEY `editor_id_FK1` (`editor_id`);

--
-- Indexes for table `editors`
--
ALTER TABLE `editors`
  ADD PRIMARY KEY (`editor_id`);

--
-- Indexes for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD PRIMARY KEY (`enrollment_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `quizzes`
--
ALTER TABLE `quizzes`
  ADD PRIMARY KEY (`question_id`,`course_id`),
  ADD KEY `course_id_idx` (`course_id`);

--
-- Indexes for table `suggestions`
--
ALTER TABLE `suggestions`
  ADD PRIMARY KEY (`suggestion_id`),
  ADD KEY `user_id_suggestion` (`user_id`);

--
-- Indexes for table `useranswers`
--
ALTER TABLE `useranswers`
  ADD PRIMARY KEY (`user_id`,`question_id`,`course_id`),
  ADD KEY `q_id_fk1_idx` (`question_id`),
  ADD KEY `c_id_fk3_idx` (`course_id`);

--
-- Indexes for table `userprogress`
--
ALTER TABLE `userprogress`
  ADD PRIMARY KEY (`sr_no`),
  ADD KEY `user_id_progress` (`user_id`),
  ADD KEY `course_id_progress` (`course_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `course_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `editors`
--
ALTER TABLE `editors`
  MODIFY `editor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `enrollment`
--
ALTER TABLE `enrollment`
  MODIFY `enrollment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `quizzes`
--
ALTER TABLE `quizzes`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `suggestions`
--
ALTER TABLE `suggestions`
  MODIFY `suggestion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `userprogress`
--
ALTER TABLE `userprogress`
  MODIFY `sr_no` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `coursepages`
--
ALTER TABLE `coursepages`
  ADD CONSTRAINT `course_id_reference` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `editor_id_FK1` FOREIGN KEY (`editor_id`) REFERENCES `editors` (`editor_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD CONSTRAINT `course_id` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `quizzes`
--
ALTER TABLE `quizzes`
  ADD CONSTRAINT `course_id_quizzes` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE;

--
-- Constraints for table `suggestions`
--
ALTER TABLE `suggestions`
  ADD CONSTRAINT `user_id_suggestion` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `useranswers`
--
ALTER TABLE `useranswers`
  ADD CONSTRAINT `c_id_fk3` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  ADD CONSTRAINT `q_id_fk1` FOREIGN KEY (`question_id`) REFERENCES `quizzes` (`question_id`),
  ADD CONSTRAINT `u_id_fk2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `userprogress`
--
ALTER TABLE `userprogress`
  ADD CONSTRAINT `course_id_progress` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `user_id_progress` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
