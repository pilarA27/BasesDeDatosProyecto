from db_config import get_connection

def run_query(sql, params=None, fetch=False):
    cn = get_connection()
    try:
        cur = cn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        if fetch:
            rows = cur.fetchall()
            return rows
        else:
            cn.commit()
            return cur.rowcount
    finally:
        cn.close()

#PARTICIPANTE
def alta_participante(ci, nombre, apellido, email):
    sql = "INSERT INTO participante (ci, nombre, apellido, email) VALUES (%s, %s, %s, %s)"
    return run_query(sql, (ci, nombre, apellido, email))

def listar_participantes():
    return run_query("SELECT * FROM participante ORDER BY apellido, nombre", fetch=True)

def modificar_participante(ci, nombre, apellido, email):
    sql = "UPDATE participante SET nombre=%s, apellido=%s, email=%s WHERE ci=%s"
    return run_query(sql, (nombre, apellido, email, ci))

def eliminar_participante(ci):
    return run_query("DELETE FROM participante WHERE ci=%s", (ci,))

#SALA
def alta_sala(nombre_sala, id_edificio, capacidad, tipo_sala):
    return

def listar_salas():
    return

def modificar_sala(id_sala, nombre_sala, id_edificio, capacidad, tipo_sala):
    return

def eliminar_sala(id_sala):
    return

#RESERVA
def crear_reserva(id_sala, fecha, id_turno, creado_por):
    return

def agregar_participante_a_reserva(id_reserva, ci):
    return

def cancelar_reserva(id_reserva):
    return

def listar_reservas():
    return

def registrar_asistencia(id_reserva, ci):
    return

def cerrar_reserva(id_reserva):
    return

#SANCIONES
def listar_sanciones():
    return
