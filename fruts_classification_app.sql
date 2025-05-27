-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 27, 2025 at 11:34 AM
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
-- Database: `fruts_classification_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `buah`
--

CREATE TABLE `buah` (
  `id` int(11) NOT NULL,
  `nama_buah` varchar(255) DEFAULT NULL,
  `gambar_buah` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `hasil_quis`
--

CREATE TABLE `hasil_quis` (
  `id` int(11) NOT NULL,
  `nama_user` varchar(100) NOT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp(),
  `skor` int(11) NOT NULL,
  `jumlah_soal` int(11) NOT NULL,
  `jumlah_benar` int(11) NOT NULL,
  `jumlah_salah` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `kandungan_buah`
--

CREATE TABLE `kandungan_buah` (
  `id` int(11) NOT NULL,
  `id_buah` int(11) NOT NULL,
  `kandungan` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `buah`
--
ALTER TABLE `buah`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hasil_quis`
--
ALTER TABLE `hasil_quis`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kandungan_buah`
--
ALTER TABLE `kandungan_buah`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_buah` (`id_buah`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `buah`
--
ALTER TABLE `buah`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `hasil_quis`
--
ALTER TABLE `hasil_quis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `kandungan_buah`
--
ALTER TABLE `kandungan_buah`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
