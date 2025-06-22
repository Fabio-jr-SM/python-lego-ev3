'''

SEGUIDOR DE LINHA COM UM SENSOR

'''





from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveSteering
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)
sensor = ColorSensor(INPUT_1)
sensor.mode = 'COL-REFLECT'

BRANCO = 60  # Ajuste conforme seu ambiente
PRETO = 10
LIMIAR = (BRANCO + PRETO) / 2

def seguir_linha():
    while True:
        valor = sensor.reflected_light_intensity
        if valor < LIMIAR:
            steering_drive.on(0, 30)
        else:
            steering_drive.on(0, 10)

def procurar_linha():
    for direcao in [30, -30]:
        for _ in range(5):
            steering_drive.on(direcao, 10)
            sleep(0.2)
            if sensor.reflected_light_intensity < LIMIAR:
                return

try:
    while True:
        if sensor.reflected_light_intensity < LIMIAR:
            seguir_linha()
        else:
            procurar_linha()
except KeyboardInterrupt:
    steering_drive.off()
