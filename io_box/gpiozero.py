# For gpiozero lib test

from gpiozero import LED
from time import sleep

led = LED(1)

def led_prompt():
    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)


if __name__ == "__main__":
    led_prompt()
    