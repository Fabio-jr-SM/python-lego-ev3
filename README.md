# Program in Python with EV3
---

### 1. **Seguir linha e reencontrar a linha ao se perder** (com 1 sensor de cor)

```python
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
```

---

### 2. **Seguir linha com 1 sensor e resolver bifurcações por cor**

```python
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
    elif cor == 2:  # Azul
        steering.on_for_seconds(100, 30, 0.8)

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
```

---

### 3. **Detectar objeto com ultrassônico e desviar**

```python
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
```
