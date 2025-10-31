from gpiozero import PWMOutputDevice
import time

esc = PWMOutputDevice(pin=18, active_high=True, initial_value=0, frequency=50)

# Neutral pulse to arm ESC
esc.value = 0.5  # 1.5ms ~ 0.5 fraction
time.sleep(3)
