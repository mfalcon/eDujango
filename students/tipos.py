# -*- encoding: utf-8 -*-

MANIANA = 0
TARDE = 1


TURNO_CHOICES = (
    (MANIANA, 'Mañana'),
    (TARDE, 'Tarde'),
)


ROJA = 0
ROSA = 1
CELESTE = 2
VERDE = 3
NARANJA = 4


SALA_CHOICES = (
    (ROJA, 'Roja'),
    (ROSA, 'Rosa'),
    (CELESTE, 'Celeste'),
    (VERDE, 'Verde'),
    (NARANJA, 'Naranja'),
)

CONFIRMADO = 0
ESPERA = 1
CANCELADO = 2
#= 3

ESTADO_ALUMNO_SALA_CHOICES = (
    (CONFIRMADO, 'Confirmado'),
    (ESPERA, 'Lista de espera'),
    (CANCELADO, 'Cancelado'),
    #(, ''),
)

A = 0
B = 1
C = 2

SECCION_CHOICES = (
    (A, 'A'),
    (B, 'B'),
    (C, 'C'),
)
