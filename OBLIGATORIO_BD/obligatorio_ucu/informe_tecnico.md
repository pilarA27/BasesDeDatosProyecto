# Informe Técnico – Sistema de Gestión de Salas de Estudio

## 1. Decisiones de diseño
- Agregamos claves técnicas `id_*` para **sala**, **programa**, **edificio** y **reserva** por integridad y rendimiento, manteniendo campos de la letra.
- Usamos `ENUM` en MySQL para `tipo_sala`, `estado` y roles de participación.
- Reglas de negocio **en la base** con triggers y SP:
  - Capacidad, sanción activa, 3/semana, 2h/día/edificio, exenciones.
  - `cerrar_reserva()` sanciona 2 meses en no-show.
- `turno` modela bloques de 1h (1..15) 08:00–23:00.

## 2. Validaciones
- **Input**: la app de consola valida campos obligatorios.
- **DB**: checks, claves únicas y triggers.
- **Negocio**: trigger `bi_reserva_participante` y SPs.

## 3. Mejoras posibles
- Calendario base (tabla de días) y vista de disponibilidad por rango.
- Usuarios/admins con permisos diferenciados.
- Auditoría de cambios.
- API REST y front web.
- Job automático para cerrar reservas vencidas.

## 4. Bitácora
- 2025-10-27 22:33 – Versión inicial: esquema, datos, triggers, app consola, BI y docker.

## 5. Bibliografía
- Manual MySQL 8 (triggers, procedimientos, YEARWEEK)
- Documentación `mysql-connector-python`
