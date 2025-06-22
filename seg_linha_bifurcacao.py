'''


Seguir linha com 1 sensor e resolver bifurcações por cor


'''

from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveSteering
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

steering = MoveSteering(OUTPUT_B, OUTPUT_C)
sensor = ColorSensor(INPUT_1)
sensor.mode = 'COL-COLOR'

def seguir_linha():
    sensor.mode = 'COL-REFLECT'
    while True:
        valor = sensor.reflected_light_intensity
        if valor < 30:
            steering.on(0, 30)
        else:
            steering.on(0, 10)

def resolver_bifurcacao():
    cor = sensor.color
    if cor == 3:  # Verde
        steering.on_for_seconds(-100, 30, 0.8)

try:
    while True:
        sensor.mode = 'COL-COLOR'
        cor = sensor.color
        if cor in [2, 3]:  # Azul ou Verde
            resolver_bifurcacao()
        else:
            seguir_linha()
except KeyboardInterrupt:
    steering.off()
