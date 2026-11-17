import os
# =====================================================
# PROYECTO: MESA DE PARTES DIGITAL
# I.E. 2032 MANUEL SCORZA TORRES
# CURSO: FUNDAMENTOS DE PROGRAMACION
# =====================================================

RUTA_ARCHIVO = "datos/expedientes.txt"


def cargar_archivo(ruta):
    cod = []
    dni_a = []
    nom_a = []
    dni_e = []
    nom_e = []
    tram = []
    fec = []

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                partes = linea.strip().split("|")

                if len(partes) != 7:
                    print(f"Linea {numero_linea} invalida. Se omite.")
                    continue

                try:
                    codigo = int(partes[0])
                    tipo_tramite = int(partes[5])

                    if tipo_tramite not in range(1, 5):
                        continue

                except ValueError:
                    print(f"Datos invalidos en linea {numero_linea}.")
                    continue

                cod.append(codigo)
                dni_a.append(partes[1])
                nom_a.append(partes[2])
                dni_e.append(partes[3])
                nom_e.append(partes[4])
                tram.append(tipo_tramite)
                fec.append(partes[6])

    except FileNotFoundError:
        print("No existe un archivo previo. Se iniciara sin expedientes.")

    n = len(cod)

    return cod, dni_a, nom_a, dni_e, nom_e, tram, fec, n


# =====================================================
# PARTE 2. GUARDAR LOS EXPEDIENTES EN EL ARCHIVO
# =====================================================

def guardar_archivo(ruta, cod, dni_a, nom_a,
                    dni_e, nom_e, tram, fec, n):

    carpeta = os.path.dirname(ruta)

    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:

        for i in range(n):
            linea = (
                f"{cod[i]}|{dni_a[i]}|{nom_a[i]}|"
                f"{dni_e[i]}|{nom_e[i]}|{tram[i]}|{fec[i]}\n"
            )

            archivo.write(linea)

    print("Los expedientes se guardaron correctamente.")


# =====================================================
# FUNCIONES DE VALIDACION Y AUXILIARES
# =====================================================

def validar_dni(dni):
    return len(dni) == 8 and dni.isdigit()


def validar_texto(texto):
    return len(texto.strip()) > 0 and "|" not in texto


def validar_tramite(opcion):
    return opcion in (1, 2, 3, 4)


def nombre_tramite(opcion):
    tramites = {
        1: "Constancia de matricula",
        2: "Constancia de vacante",
        3: "Certificado de estudios",
        4: "Ficha unica de matricula (FUM)"
    }

    return tramites.get(opcion, "Desconocido")


def generar_codigo(cod):
    mayor = 0
    for c in cod:
        if c > mayor:
            mayor = c
    return mayor + 1


# =====================================================
# REGISTRAR EXPEDIENTE
# =====================================================

def registrar_expediente(cod, dni_a, nom_a,
                         dni_e, nom_e, tram, fec, n):

    print("\n--- REGISTRO DE NUEVO EXPEDIENTE ---")

    if n >= 100:
        print("Se alcanzo el limite de 100 expedientes.")
        return n

    # Generación automática del código (max + 1) según las indicaciones
    codigo = generar_codigo(cod)

    while True:
        dni_apoderado = input("DNI del apoderado: ").strip()

        if validar_dni(dni_apoderado):
            break

        print("El DNI debe contener exactamente 8 digitos.")

    while True:
        nombre_apoderado = input("Nombre del apoderado: ").strip().upper()

        if validar_texto(nombre_apoderado):
            break

        print("Ingrese un nombre valido.")

    while True:
        dni_estudiante = input("DNI del estudiante: ").strip()

        if validar_dni(dni_estudiante):
            break

        print("El DNI debe contener exactamente 8 digitos.")

    while True:
        nombre_estudiante = input("Nombre del estudiante: ").strip().upper()

        if validar_texto(nombre_estudiante):
            break

        print("Ingrese un nombre valido.")

    print("\nTIPOS DE TRAMITE")
    print("1. Constancia de matricula")
    print("2. Constancia de vacante")
    print("3. Certificado de estudios")
    print("4. Ficha unica de matricula (FUM)")

    while True:
        try:
            tipo = int(input("Seleccione el tipo de tramite: "))

            if validar_tramite(tipo):
                break

            print("Seleccione una opcion entre 1 y 4.")

        except ValueError:
            print("Ingrese un numero valido.")

    fecha = input("Fecha de recepcion (DD/MM/AAAA): ").strip()

    cod.append(codigo)
    dni_a.append(dni_apoderado)
    nom_a.append(nombre_apoderado)
    dni_e.append(dni_estudiante)
    nom_e.append(nombre_estudiante)
    tram.append(tipo)
    fec.append(fecha)

    n += 1

    print("\nExpediente registrado correctamente. Codigo asignado: EXP-" + str(codigo))
    return n


# =====================================================
# CONSULTAR EXPEDIENTE POR CODIGO
# =====================================================

def consultar_expediente(cod, dni_a, nom_a,
                         dni_e, nom_e, tram, fec, n):

    print("\n--- CONSULTA DE EXPEDIENTE ---")

    try:
        codigo = int(input("Ingrese el codigo que desea consultar: "))
    except ValueError:
        print("Codigo invalido.")
        return

    for i in range(n):

        if cod[i] == codigo:
            print("\nEXPEDIENTE ENCONTRADO")
            print("--------------------------------")
            print("Codigo: EXP-", cod[i], sep="")
            print("DNI apoderado:", dni_a[i])
            print("Apoderado:", nom_a[i])
            print("DNI estudiante:", dni_e[i])
            print("Estudiante:", nom_e[i])
            print("Tramite:", nombre_tramite(tram[i]))
            print("Fecha de recepcion:", fec[i])
            return

    print("No se encontro el expediente solicitado.")


# =====================================================
# ORDENAR EXPEDIENTES POR CODIGO
# METODO DE BURBUJA
# =====================================================

def ordenar_por_codigo(cod, dni_a, nom_a,
                       dni_e, nom_e, tram, fec, n):

    for i in range(n - 1):

        for j in range(n - 1 - i):

            if cod[j] > cod[j + 1]:

                cod[j], cod[j + 1] = cod[j + 1], cod[j]
                dni_a[j], dni_a[j + 1] = dni_a[j + 1], dni_a[j]
                nom_a[j], nom_a[j + 1] = nom_a[j + 1], nom_a[j]
                dni_e[j], dni_e[j + 1] = dni_e[j + 1], dni_e[j]
                nom_e[j], nom_e[j + 1] = nom_e[j + 1], nom_e[j]
                tram[j], tram[j + 1] = tram[j + 1], tram[j]
                fec[j], fec[j + 1] = fec[j + 1], fec[j]

    print("Expedientes ordenados correctamente.")


# =====================================================
# LISTAR TODOS LOS EXPEDIENTES
# =====================================================

def listar_expedientes(cod, dni_a, nom_a,
                       dni_e, nom_e, tram, fec, n):

    print("\n--- EXPEDIENTES REGISTRADOS ---")

    if n == 0:
        print("No hay expedientes registrados.")
        return

    for i in range(n):

        print("\n--------------------------------")
        print("Codigo: EXP-", cod[i], sep="")
        print("DNI apoderado:", dni_a[i])
        print("Apoderado:", nom_a[i])
        print("DNI estudiante:", dni_e[i])
        print("Estudiante:", nom_e[i])
        print("Tramite:", nombre_tramite(tram[i]))
        print("Fecha de recepcion:", fec[i])


# =====================================================
# MOSTRAR RESUMEN DE EXPEDIENTES
# =====================================================

def mostrar_resumen(tram, n):

    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0

    for tipo in tram:

        if tipo == 1:
            c1 += 1
        elif tipo == 2:
            c2 += 1
        elif tipo == 3:
            c3 += 1
        elif tipo == 4:
            c4 += 1

    print("\n--- RESUMEN DE ATENCIONES ---")
    print("Total de expedientes:", n)
    print("Constancia de matricula:", c1)
    print("Constancia de vacante:", c2)
    print("Certificado de estudios:", c3)
    print("Ficha unica de matricula (FUM):", c4)


# =====================================================
# PARTE 3. PROGRAMA PRINCIPAL
# =====================================================

def main():

    # Cargar los datos al iniciar
    cod, dni_a, nom_a, dni_e, nom_e, tram, fec, n = (
        cargar_archivo(RUTA_ARCHIVO)
    )

    while True:

        print("\n=====================================")
        print(" MESA DE PARTES DIGITAL - I.E. 2032")
        print("=====================================")
        print("1. Registrar expediente")
        print("2. Consultar expediente por codigo")
        print("3. Ordenar por codigo y listar")
        print("4. Ver resumen")
        print("5. Guardar")
        print("6. Guardar y salir")

        try:
            opcion = int(input("Seleccione una opcion (1-6): "))

        except ValueError:
            print("Ingrese una opcion numerica valida.")
            continue

        if opcion == 1:

            n = registrar_expediente(
                cod, dni_a, nom_a, dni_e, nom_e, tram, fec, n
            )

        elif opcion == 2:

            consultar_expediente(
                cod, dni_a, nom_a, dni_e, nom_e, tram, fec, n
            )

        elif opcion == 3:

            ordenar_por_codigo(
                cod, dni_a, nom_a, dni_e, nom_e, tram, fec, n
            )

            listar_expedientes(
                cod, dni_a, nom_a, dni_e, nom_e, tram, fec, n
            )

        elif opcion == 4:

            mostrar_resumen(tram, n)

        elif opcion == 5:

            guardar_archivo(
                RUTA_ARCHIVO, cod, dni_a, nom_a,
                dni_e, nom_e, tram, fec, n
            )

        elif opcion == 6:

            guardar_archivo(
                RUTA_ARCHIVO, cod, dni_a, nom_a,
                dni_e, nom_e, tram, fec, n
            )

            print("Saliendo del sistema. Gracias por utilizarlo.")
            break

        else:

            print("Opcion no valida. Intente nuevamente.")


# =====================================================
# EJECUTAR EL SISTEMA
# =====================================================

if __name__ == "__main__":
    main()
