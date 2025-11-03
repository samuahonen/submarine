import RPi.GPIO as GPIO
import time

# Pin where ESC signal wire is connected
ESC_PIN = 12  # You can use any valid PWM pin (e.g. GPIO12, GPIO13, GPIO18, GPIO19)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN, GPIO.OUT)

# Create PWM object, 50Hz (20ms period)
pwm = GPIO.PWM(ESC_PIN, 50)
pwm.start(0)

def set_speed(microseconds):
    # Convert 1000–2000 µs to duty cycle percentage
    duty = (microseconds / 20000) * 100
    pwm.ChangeDutyCycle(duty)

try:
    print("Starting ESC...")
    set_speed(1000)
    time.sleep(3)
    print("Ready! Increasing speed...")

    # Ramp up
    for speed in range(1000, 2001, 10):
        set_speed(speed)
        print(f"Speed: {speed}")
        time.sleep(0.02)

    # Ramp down
    for speed in range(2000, 999, -10):
        set_speed(speed)
        print(f"Speed: {speed}")
        time.sleep(0.02)

finally:
    pwm.stop()
    GPIO.cleanup()
