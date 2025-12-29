import pigpio
import time

# --- CONFIGURATION ---
# We map each pin to its specific name and its specific STOP (Neutral) value.
# 20 & 21 use 1480, the rest use 1500.
MOTORS = {
    # Lift Motors
    20: {'name': 'Lift Left',   'neutral': 1480},
    21: {'name': 'Lift Right',  'neutral': 1480},
    16: {'name': 'Lift Center', 'neutral': 1500},
    
    # Drive Motors
    23: {'name': 'Drive Left',  'neutral': 1500},
    24: {'name': 'Drive Right', 'neutral': 1500}
}

# --- SETUP ---
pi = pigpio.pi()

if not pi.connected:
    print("Pigpio daemon is not running. Run: sudo pigpiod")
    exit()

def set_motor(pin, micros):
    """Sets a specific pin to a pulse width safely."""
    # Hard safety limits
    if micros < 1000: micros = 1000
    if micros > 2000: micros = 2000
    pi.set_servo_pulsewidth(pin, micros)

def stop_all_motors():
    """Sends the specific NEUTRAL signal to every motor."""
    print("Stopping all motors...")
    for pin, config in MOTORS.items():
        neutral_pulse = config['neutral']
        pi.set_servo_pulsewidth(pin, neutral_pulse)

try:
    print("--- ROBOT INITIALIZATION ---")
    
    # 1. Arming Sequence (Sending Neutral to all ESCs)
    print("Arming ESCs with their specific neutral values...")
    stop_all_motors()
    
    print("Waiting 3 seconds for ESCs to beep/initialize...")
    time.sleep(3)
    print("Ready!")
    print("----------------------------")
    print("Commands:")
    print("  'lift'  - Test Lift motors (20, 21, 16)")
    print("  'drive' - Test Drive motors (23, 24)")
    print("  'stop'  - Stop everything")
    print("  'q'     - Quit")
    
    while True:
        cmd = input("\nEnter Command: ").lower()
        
        if cmd == 'q':
            break
            
        elif cmd == 'stop':
            stop_all_motors()
            
        elif cmd == 'lift':
            speed = int(input("  Enter Lift Speed (e.g. 1600 for up, 1400 down): "))
            # Apply to all lift pins
            # Note: 20 and 21 usually move together
            set_motor(20, speed) 
            set_motor(21, speed) 
            set_motor(16, speed)
            print(f"  Lift set to {speed}")

        elif cmd == 'drive':
            speed = int(input("  Enter Drive Speed (e.g. 1600): "))
            set_motor(23, speed)
            set_motor(24, speed)
            print(f"  Drive set to {speed}")
            
        else:
            print("Unknown command.")

except ValueError:
    print("Please enter valid numbers for speed.")

except KeyboardInterrupt:
    print("\nEmergency Stop triggered!")

finally:
    print("Cleaning up...")
    stop_all_motors() # Ensure everything stops correctly
    time.sleep(0.5)
    # Turn off signal generation
    for pin in MOTORS:
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()