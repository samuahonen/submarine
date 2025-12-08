import RPi.GPIO as GPIO
import time

# ESC PWM pin configuration
ESC_PIN = 18

# ESC pulse width range (microseconds)
MIN_PULSE = 1000
NEUTRAL_PULSE = 1500
MAX_PULSE = 2000

# PWM frequency (Hz)
PWM_FREQ = 50


def pulse_to_duty(microseconds):
    """Convert microseconds to duty cycle percentage for 50Hz PWM."""
    return (microseconds / 20000) * 100


def initialize_esc(pwm, wait_time=3):
    """Initialize ESC by sending neutral signal and waiting."""
    print("Initializing ESC...")
    print(f"Sending neutral signal ({NEUTRAL_PULSE}µs) for {wait_time}s")
    pwm.ChangeDutyCycle(pulse_to_duty(NEUTRAL_PULSE))
    time.sleep(wait_time)
    print("ESC ready!")


def test_ramp_up_down(pwm):
    """Test ESC by ramping speed up and down."""
    print("\n--- Ramping UP ---")
    for speed in range(NEUTRAL_PULSE, MAX_PULSE + 1, 50):
        pwm.ChangeDutyCycle(pulse_to_duty(speed))
        print(f"Speed: {speed}µs")
        time.sleep(0.5)
    
    print("\n--- Ramping DOWN ---")
    for speed in range(MAX_PULSE, NEUTRAL_PULSE - 1, -50):
        pwm.ChangeDutyCycle(pulse_to_duty(speed))
        print(f"Speed: {speed}µs")
        time.sleep(0.5)
    
    print("\n--- Testing REVERSE ---")
    for speed in range(NEUTRAL_PULSE, MIN_PULSE - 1, -50):
        pwm.ChangeDutyCycle(pulse_to_duty(speed))
        print(f"Speed: {speed}µs")
        time.sleep(0.5)
    
    print("\n--- Back to NEUTRAL ---")
    pwm.ChangeDutyCycle(pulse_to_duty(NEUTRAL_PULSE))
    print(f"Speed: {NEUTRAL_PULSE}µs")
    time.sleep(1)


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ESC_PIN, GPIO.OUT)
    
    pwm = GPIO.PWM(ESC_PIN, PWM_FREQ)
    pwm.start(0)
    
    try:
        initialize_esc(pwm, wait_time=3)
        test_ramp_up_down(pwm)
        print("\nTest complete!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        
    finally:
        print("Cleaning up...")
        pwm.ChangeDutyCycle(pulse_to_duty(NEUTRAL_PULSE))
        time.sleep(0.5)
        pwm.stop()
        GPIO.cleanup()
        print("Done!")


if __name__ == "__main__":
    main()