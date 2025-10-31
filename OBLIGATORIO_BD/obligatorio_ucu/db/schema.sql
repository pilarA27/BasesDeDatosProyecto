-- MySQL 8.x
-- Sistema para Gestión de Salas de Estudio - UCU
-- Esquema base + restricciones mínimas. Sin ORM. Validaciones adicionales en disparadores.

SET NAMES utf8mb4;
SET time_zone = '+00:00';

DROP DATABASE IF EXISTS ucu_salas;
CREATE DATABASE ucu_salas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ucu_salas;

-- Catálogos y entidades principales

CREATE TABLE facultad (
  id_facultad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE programa_academico (
  id_programa INT AUTO_INCREMENT PRIMARY KEY,
  nombre_programa VARCHAR(150) NOT NULL UNIQUE,
  id_facultad INT NOT NULL,
  tipo ENUM('grado','posgrado') NOT NULL,
  FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

CREATE TABLE participante (
  ci VARCHAR(20) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE
);

-- rol a nivel programa (docente/alumno) y mapea participante con programa
CREATE TABLE participante_programa_academico (
  id_alumno_programa INT AUTO_INCREMENT PRIMARY KEY,
  ci_participante VARCHAR(20) NOT NULL,
  id_programa INT NOT NULL,
  rol ENUM('alumno','docente') NOT NULL,
  UNIQUE KEY uniq_pp (ci_participante, id_programa, rol),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_programa) REFERENCES programa_academico(id_programa)
);

CREATE TABLE login (
  correo VARCHAR(150) PRIMARY KEY,
  contrasena VARCHAR(255) NOT NULL,
  ci_participante VARCHAR(20) NOT NULL,
  FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);

CREATE TABLE edificio (
  id_edificio INT AUTO_INCREMENT PRIMARY KEY,
  nombre_edificio VARCHAR(120) NOT NULL UNIQUE,
  direccion VARCHAR(200),
  departamento VARCHAR(80)
);

-- Añadimos id_sala para integridad y rendimiento, manteniendo campos solicitados
CREATE TABLE sala (
  id_sala INT AUTO_INCREMENT PRIMARY KEY,
  nombre_sala VARCHAR(120) NOT NULL,
  id_edificio INT NOT NULL,
  capacidad INT NOT NULL CHECK (capacidad > 0),
  tipo_sala ENUM('libre','posgrado','docente') NOT NULL,
  UNIQUE KEY uniq_sala (id_edificio, nombre_sala),
  FOREIGN KEY (id_edificio) REFERENCES edificio(id_edificio)
);

-- Turnos de 1h entre 08:00 y 23:00 (último 22-23)
CREATE TABLE turno (
  id_turno INT PRIMARY KEY,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  CHECK (TIMESTAMPDIFF(MINUTE, hora_inicio, hora_fin) = 60)
);

CREATE TABLE reserva (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  id_sala INT NOT NULL,
  fecha DATE NOT NULL,
  id_turno INT NOT NULL,
  estado ENUM('activa','cancelada','sin_asistencia','finalizada') NOT NULL DEFAULT 'activa',
  creado_por VARCHAR(20) NOT NULL, -- ci del creador
  creado_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uniq_slot (id_sala, fecha, id_turno),
  FOREIGN KEY (id_sala) REFERENCES sala(id_sala),
  FOREIGN KEY (id_turno) REFERENCES turno(id_turno),
  FOREIGN KEY (creado_por) REFERENCES participante(ci)
);

CREATE TABLE reserva_participante (
  id_reserva INT NOT NULL,
  ci_participante VARCHAR(20) NOT NULL,
  fecha_solicitud_reserva TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  asistencia TINYINT(1) NOT NULL DEFAULT 0,
  checkin_ts TIMESTAMP NULL,
  PRIMARY KEY (id_reserva, ci_participante),
  FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva) ON DELETE CASCADE,
  FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);

CREATE TABLE sancion_participante (
  id_sancion INT AUTO_INCREMENT PRIMARY KEY,
  ci_participante VARCHAR(20) NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  motivo VARCHAR(255) NOT NULL,
  id_reserva INT NULL,
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva),
  CHECK (fecha_fin > fecha_inicio)
);

-- Índices útiles
CREATE INDEX idx_reserva_fecha ON reserva(fecha);
CREATE INDEX idx_reserva_estado ON reserva(estado);
CREATE INDEX idx_rp_ci ON reserva_participante(ci_participante);
CREATE INDEX idx_sancion_ci ON sancion_participante(ci_participante);
