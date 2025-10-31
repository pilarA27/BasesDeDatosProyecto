import sys
from funciones_abm import (
    alta_participante, listar_participantes, modificar_participante, eliminar_participante,
    alta_sala, listar_salas, modificar_sala, eliminar_sala,
    crear_reserva, agregar_participante_a_reserva, cancelar_reserva, listar_reservas,
    registrar_asistencia, cerrar_reserva, listar_sanciones
)
from consultas_bi import ejecutar_bi

def input_nonempty(prompt):
    val = input(prompt).strip()
    if not val:
        raise ValueError("Valor requerido.")
    return val

def menu_participantes():
    while True:
        print("\nPARTICIPANTES")
        print("1. Alta")
        print("2. Listar")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            ci = input_nonempty("CI: ")
            nombre = input_nonempty("Nombre: ")
            apellido = input_nonempty("Apellido: ")
            email = input("Email: ").strip() or None
            try:
                alta_participante(ci, nombre, apellido, email)
                print("Participante creado.")
            except Exception as e:
                print("ERROR:", e)
        elif op == "2":
            rows = listar_participantes()
            for r in rows:
                print(r)
        elif op == "3":
            ci = input_nonempty("CI: ")
            nombre = input_nonempty("Nuevo nombre: ")
            apellido = input_nonempty("Nuevo apellido: ")
            email = input("Nuevo email: ").strip() or None
            try:
                modificar_participante(ci, nombre, apellido, email)
                print("Participante modificado.")
            except Exception as e:
                print("ERROR:", e)
        elif op == "4":
            ci = input_nonempty("CI: ")
            try:
                eliminar_participante(ci)
                print("Participante eliminado.")
            except Exception as e:
                print("ERROR:", e)
        elif op == "0":
            return
        else:
            print("Opción inválida.")

def menu_salas():
    while True:
        print("\nSALAS")
        print("1. Alta")
        print("2. Listar")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            nombre = input_nonempty("Nombre sala: ")
            id_edificio = input_nonempty("ID edificio: ")
            capacidad = input_nonempty("Capacidad (int): ")
            tipo = input_nonempty("Tipo (libre/posgrado/docente): ")
            try:
                alta_sala(nombre, int(id_edificio), int(capacidad), tipo)
                print("OK: sala creada.")
            except Exception as e:
                print("ERROR:", e)
        elif op == "2":
            rows = listar_salas()
            for r in rows:
                print(r)
        elif op == "3":
            id_sala = int(input_nonempty("ID sala: "))
            nombre = input_nonempty("Nuevo nombre sala: ")
            id_edificio = int(input_nonempty("Nuevo ID edificio: "))
            capacidad = int(input_nonempty("Nueva capacidad: "))
            tipo = input_nonempty("Nuevo tipo (libre/posgrado/docente): ")
            try:
                modificar_sala(id_sala, nombre, id_edificio, capacidad, tipo)
                print("Sala modificada.")
            except Exception as e:
                print("ERROR:", e)
        elif op == "4":
            id_sala = int(input_nonempty("ID sala: "))
            try:
                eliminar_sala(id_sala)
                print("Sala eliminada.")
            except Exception as e:
                print("ERROR:", e)
        elif op == "0":
            return
        else:
            print("Opción inválida.")

def menu_reservas():
    while True:
        print("\nRESERVAS")
        print("1. Crear reserva")
        print("2. Agregar participante a reserva")
        print("3. Listar reservas")
        print("4. Cancelar reserva")
        print("5. Registrar asistencia")
        print("6. Cerrar reserva")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                id_sala = int(input_nonempty("ID sala: "))
                fecha = input_nonempty("Fecha (YYYY-MM-DD): ")
                id_turno = int(input_nonempty("ID turno (1..15): "))
                creador = input_nonempty("CI creador: ")
                crear_reserva(id_sala, fecha, id_turno, creador)
                print("Reserva creada.")
            elif op == "2":
                id_reserva = int(input_nonempty("ID reserva: "))
                ci = input_nonempty("CI: ")
                agregar_participante_a_reserva(id_reserva, ci)
                print("Participante agregado.")
            elif op == "3":
                for r in listar_reservas():
                    print(r)
            elif op == "4":
                id_reserva = int(input_nonempty("ID reserva: "))
                cancelar_reserva(id_reserva)
                print("Reserva cancelada.")
            elif op == "5":
                id_reserva = int(input_nonempty("ID reserva: "))
                ci = input_nonempty("CI: ")
                registrar_asistencia(id_reserva, ci)
                print("Asistencia registrada.")
            elif op == "6":
                id_reserva = int(input_nonempty("ID reserva: "))
                cerrar_reserva(id_reserva)
                print("Reserva cerrada.")
            elif op == "0":
                return
            else:
                print("Opción inválida.")
        except Exception as e:
            print("ERROR:", e)

def menu_bi():
    while True:
        print("\nREPORTES BI")
        print("1. Salas más reservadas")
        print("2. Turnos más demandados")
        print("3. Promedio de participantes por sala")
        print("4. Reservas por carrera y facultad")
        print("5. % ocupación por edificio")
        print("6. Reservas y asistencias por tipo participante")
        print("7. Sanciones por tipo participante")
        print("8. % efectivas vs no efectivas")
        print("9. Tasa de uso efectivo por semana")
        print("10. Top 5 participantes más activos")
        print("11. Promedio horas por edificio y semana")
        print("0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            return
        try:
            data = ejecutar_bi(int(op))
            for row in data:
                print(row)
        except Exception as e:
            print("ERROR:", e)

def main():
    while True:
        print("\nGESTIÓN DE SALAS DE ESTUDIO")
        print("1. Participantes")
        print("2. Salas")
        print("3. Reservas")
        print("4. Sanciones (listar)")
        print("5. Reportes BI")
        print("0. Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_participantes()
        elif op == "2":
            menu_salas()
        elif op == "3":
            menu_reservas()
        elif op == "4":
            for s in listar_sanciones():
                print(s)
        elif op == "5":
            menu_bi()
        elif op == "0":
            print("Chau!")
            sys.exit(0)
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
