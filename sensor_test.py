import time

from hcsr04 import HCSR04
from machine import Pin, I2C


sensor = HCSR04(trigger_pin=22, echo_pin=23, echo_timeout_us=1000000)
led_green = Pin(27, mode=Pin.OUT)
led_red = Pin(21, mode=Pin.OUT)

try:
    led_red(0)
    led_green(1)
    while True:
        distance = sensor.distance_cm()
        print(distance)
        if distance < 5:
            led_green(0)
            led_red(1)
            time.sleep(5)
            led_red(0)
            time.sleep(1)
            led_green(1)

except KeyboardInterrupt:
    pass
