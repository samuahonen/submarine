import pigpio
import time

# --- SETUP ---
# Connect to the local hardware daemon
pi = pigpio.pi()

# Check if daemon is running
if not pi.connected:
    print("Pigpio daemon is not running. Did you run 'sudo pigpiod'?")
    exit()

try:
    print("--- PRECISE MOTOR TESTER (PIGPIO) ---")
    print("  Lift:  Left=20, Right=21, Center=16")
    print("  Drive: Left=23, Right=24")
    print("---------------------------------------")

    pin_str = input("Enter GPIO Pin number to test: ")
    pin = int(pin_str)
    
    # Send neutral signal immediately to initialize ESC
    # 0 = Off, 1500 = Neutral
    print(f"Initializing Pin {pin} to 1500us...")
    pi.set_servo_pulsewidth(pin, 1500)
    time.sleep(2) # Give ESC time to recognize the signal
    
    print("\n--- TEST MODE ---")
    
    while True:
        user_input = input("Enter Speed (1000-2000) or 'q': ")
        
        if user_input.lower() == 'q':
            break
            
        try:
            micros = int(user_input)
            
            # Safety limits
            if micros < 1000: micros = 1000
            if micros > 2000: micros = 2000
            
            print(f"Setting Pin {pin} to {micros}us")
            
            # Pigpio function sets width directly in microseconds
            pi.set_servo_pulsewidth(pin, micros)
            
        except ValueError:
            print("Invalid number.")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    print("Cleaning up...")
    # Stop the signal generation on the pin (0 pulse width)
    pi.set_servo_pulsewidth(pin, 0)
    # Stop the connection to the daemon
    pi.stop()