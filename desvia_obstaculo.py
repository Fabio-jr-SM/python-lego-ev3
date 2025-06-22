'''


Detectar objeto com ultrassônico e desviar


'''


from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_4
from time import sleep

motores = MoveTank(OUTPUT_B, OUTPUT_C)
ultrassom = UltrasonicSensor(INPUT_4)

DISTANCIA_LIMITE = 20  # cm

def desviar():
    motores.on_for_seconds(left_speed=-30, right_speed=30, seconds=0.7)  # virar
    motores.on_for_seconds(left_speed=30, right_speed=30, seconds=1.0)  # andar reto
    motores.on_for_seconds(left_speed=30, right_speed=-30, seconds=0.7)  # voltar para a linha

try:
    while True:
        distancia = ultrassom.distance_centimeters
        if distancia < DISTANCIA_LIMITE:
            motores.off()
            desviar()
        else:
            motores.on(30, 30)
except KeyboardInterrupt:
    motores.off()
