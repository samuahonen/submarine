import RPi.GPIO as GPIO
import time

# --- SETUP ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def set_servo_pulse(pwm, pulse_width_us):
    """
    Converts microseconds (1000-2000) to Duty Cycle (0-100%)
    Frequency is 50Hz (20ms total period)
    """
    duty_cycle = (pulse_width_us / 20000) * 100
    pwm.ChangeDutyCycle(duty_cycle)

try:
    print("--- SIMPLE MOTOR TESTER ---")
    print("Available Pins based on your code:")
    print("  Lift:  Left=20, Right=21, Center=16")
    print("  Drive: Left=23, Right=24")
    print("-----------------------------")

    # 1. Select the Pin
    pin = int(input("Enter GPIO Pin number to test: "))
    
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50) # 50Hz frequency
    
    # 2. Arming Sequence
    print("\nAttempting to ARM the ESC...")
    print("Sending 1500us (Neutral) signal.")
    
    pwm.start(0) # Start PWM
    set_servo_pulse(pwm, 1500) # Send Neutral immediately
    
    print(">>> LISTEN NOW: You should hear 'Beep-Beep' from the motor.")
    print(">>> Waiting 3 seconds for arming...")
    time.sleep(3)
    
    # 3. Manual Control Loop
    print("\n--- TEST MODE ---")
    print("Enter pulse width (1000 to 2000).")
    print("Type '1500' to Stop.")
    print("Type 'q' to quit.")
    
    while True:
        user_input = input("Enter Speed (1000-2000): ")
        
        if user_input.lower() == 'q':
            break
            
        try:
            micros = int(user_input)
            
            # Safety checks
            if micros < 1000: micros = 1000
            if micros > 2000: micros = 2000
            
            print(f"Setting Pin {pin} to {micros}us")
            set_servo_pulse(pwm, micros)
            
        except ValueError:
            print("Invalid number.")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # 4. Clean Shutdown (Prevents the error you saw earlier)
    print("Cleaning up GPIO...")
    try:
        pwm.stop()
    except:
        pass
    GPIO.cleanup()