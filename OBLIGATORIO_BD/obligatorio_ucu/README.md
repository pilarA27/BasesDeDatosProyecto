# Sistema de Gestión de Salas de Estudio – UCU (Console)

**Backend:** Python 3.11 (sin ORM, `mysql-connector-python`)  
**Base:** MySQL 8  
**Modo:** Consola interactiva  
**Docker:** docker-compose (db + app)

## Estructura
```
obligatorio_ucu/
├── db/
│   ├── schema.sql
│   ├── triggers_procedures.sql
│   ├── data_seed.sql
│   └── queries_bi.sql
├── app/
│   ├── main.py
│   ├── db_config.py
│   ├── funciones_abm.py
│   └── consultas_bi.py
└── docker-compose.yml
```

## Requisitos
- Docker y Docker Compose

## Cómo correr
```bash
cd obligatorio_ucu
docker compose up -d db
# Esperá ~15-25s a que inicialice MySQL con los .sql
docker compose up app
```
> El servicio **app** abre el menú de consola. Podés interactuar con el teclado.

## Datos cargados
- **Edificios:** Sede Central / Punta Carretas  
- **Salas:** 5 (3 libres, 1 posgrado, 1 docente)  
- **Participantes:** 6 (grado x3, posgrado x2, docente x1)  
- **Turnos:** 1..15 entre 08:00–23:00  
- **Reservas demo:** en fechas relativas a *hoy*

## Reglas y validaciones
- Capacidad de sala.
- Sanción activa impide participar.
- Máx **3 reservas activas** por semana por participante (exentos: docente en sala docente; alumno posgrado en sala posgrado).
- Máx **2 horas diarias por edificio** por participante (exentos idem).
- **Cierre de reserva** (`CALL cerrar_reserva(id)`): si nadie asistió → estado `sin_asistencia` y sanción de **2 meses** a todos los inscriptos.

## Operaciones clave (Consola)
- **Participantes:** Alta/Mod/Del/List
- **Salas:** Alta/Mod/Del/List
- **Reservas:** Crear, Agregar participante, Cancelar, Registrar asistencia, Cerrar
- **Sanciones:** Listar
- **Reportes BI:** 1..11 (las 8 pedidas + 3 extra)

## Notas
- Los *CHECK* se aplican en MySQL 8.
- Si ajustás zonas horarias/horarios, actualizá la tabla `turno`.
- La vista `vw_disponibilidad_bloques` muestra disponibilidad por fecha/sala/turno para fechas ya creadas en `reserva` (podés extender generando un calendario de días).

## Defensa (sugerencias)
- Mostrar **violación de reglas** en vivo (intentar 3ª hora en mismo día y edificio).
- Mostrar **exención** con sala posgrado/docente.
- Ejecutar `CALL cerrar_reserva(id)` en una reserva sin asistencia y ver sanciones.
