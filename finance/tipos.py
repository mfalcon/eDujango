# -*- encoding: utf-8 -*-

CUOTA_BASE = 0
DOBLE_JORNADA = 1
COMEDOR = 2
COMPUTACION = 3
INGLES = 4
TALLER = 5
CUOTA_BASE_2 = 6
DOBLE_JORNADA_2 = 7


TIPO_CHOICES = (
    (CUOTA_BASE, 'Cuota base'),
    (DOBLE_JORNADA, 'Doble Jornada'), # se le suma $x a cuota base
    (CUOTA_BASE_2, 'Cuota base(Sala de 2)'),
    (DOBLE_JORNADA_2, 'Doble Jornada(Sala de 2)'), # se le suma $x a cuota base
    (COMEDOR, 'Comedor'),
    #(COMPUTACION, 'Computación'),
    #(INGLES, 'Inglés'),
    #(TALLER, 'Taller'),
)


MATRICULA = 0
REMERA = 1
PANTALON_A = 2
PANTALON_B = 3
BUZO_A = 4
BUZO_B = 5
BOLSITA = 6
MATERIALES = 7
GUARDAPOLVO = 8
SHORT = 9


ELEMENTO_CHOICES = (
    (MATRICULA, 'Matrícula'),
    (REMERA, 'Remera'),
    (PANTALON_A, 'Pantalón talles 4-6'),
    (PANTALON_B, 'Pantalón talles 8-10-12'),
    (BUZO_A, 'Buzo talles 4-6'),
    (BUZO_B, 'Buzo talles 8-10-12'),
    (BOLSITA, 'Bolsita'),
    (MATERIALES, 'Materiales'),
    (GUARDAPOLVO, 'Guardapolvo'),
    (SHORT, 'Short'),
)


OWNER = 0 # cashflow, sueldos
ADMIN = 1 # secretaria(cuotas, gastos)
MAESTRA = 2 #informes, salas
RESPONSABLE = 3 #informes especificos
DIRECTORA = 4
VICEDIRECTORA = 5
PRECEPTOR = 6

USER_CHOICES = (
    (OWNER, 'Owner'),
    (ADMIN, 'Administrador'),
    (MAESTRA, 'Maestra'),
    (RESPONSABLE, 'Responsable'),
    (DIRECTORA, 'Directora'),
    (VICEDIRECTORA, 'Vice-Directora'),
    (PRECEPTOR, 'Preceptor'),
)

MADRE = 0
PADRE = 1
ABUELO = 2
TUTOR = 3
TIO = 4
ABUELA = 5
OTRO = 6

REL_CHOICES = (
    (MADRE, 'Madre'),
    (PADRE, 'Padre'),
    (ABUELO, 'Abuelo'),
    (ABUELA, 'Abuela'),
    (TUTOR, 'Tutor'),
    (TIO, 'Tío'),
    (OTRO, 'Otro'),
)

SEXO_CHOICES = (
    (0, 'Masculino'),
    (1, 'Femenino'),
)

DNI = 0 # Faltan agregar otros tipos

DOC_CHOICES = (
    (DNI, 'DNI'),
)

RECIBO = 0
FAC_C = 1

COMP_CHOICES = (
    (RECIBO, 'Recibo'),
    (FAC_C, 'Factura C'),
)

AR = 0
BR = 1
BL = 2
PG = 3
UR = 4
CL = 5
PR = 6
OTRA = 7

NAC_CHOICES = (
    (AR, 'Argentina'),
    (BR, 'Brasilera'),
    (BL, 'Boliviana'),
    (PG, 'Paraguaya'),
    (UR, 'Uruguaya'),
    (CL, 'Chilena'),
    (PR, 'Peruana'),
    (OTRA, 'Otra'),
)

BARRIO = 0
FAMILIA = 1

CONOCIO_CHOICES = (
    (BARRIO, 'Barrio'),
    (FAMILIA, 'Familia'),
)
