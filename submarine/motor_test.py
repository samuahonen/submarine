import pigpio
import time

# --- CONFIGURATION ---
# Map each pin to its specific name and STOP (Neutral) value.
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
    if micros < 1000: micros = 1000
    if micros > 2000: micros = 2000
    pi.set_servo_pulsewidth(pin, micros)

def stop_all_motors():
    """Sends the specific NEUTRAL signal to every motor."""
    for pin, config in MOTORS.items():
        neutral_pulse = config['neutral']
        pi.set_servo_pulsewidth(pin, neutral_pulse)

try:
    print("--- SINGLE MOTOR TESTER ---")
    
    # 1. Arming Sequence
    print("Arming all ESCs (Neutral)...")
    stop_all_motors()
    time.sleep(2)
    print("Ready!")
    
    while True:
        print("\n--- SELECT MOTOR ---")
        for pin, config in MOTORS.items():
            print(f"  Pin {pin}: {config['name']} (Neutral: {config['neutral']})")
        
        user_choice = input("\nEnter Pin number to test (or 'q' to quit): ")
        
        if user_choice.lower() == 'q':
            break
            
        try:
            target_pin = int(user_choice)
            if target_pin not in MOTORS:
                print("Invalid Pin Number!")
                continue
                
            motor_name = MOTORS[target_pin]['name']
            neutral_val = MOTORS[target_pin]['neutral']
            
            print(f"\n>> TESTING: {motor_name} (Pin {target_pin})")
            print(f">> Current Speed: {neutral_val} (Neutral)")
            print(">> Enter speed (1000-2000), or 'b' to go back.")
            
            # --- INDIVIDUAL MOTOR CONTROL LOOP ---
            while True:
                speed_input = input(f"   Speed for {motor_name}: ")
                
                if speed_input.lower() == 'b':
                    # Stop this specific motor before going back
                    print(f"   Stopping {motor_name}...")
                    pi.set_servo_pulsewidth(target_pin, neutral_val)
                    break
                
                try:
                    speed = int(speed_input)
                    set_motor(target_pin, speed)
                    print(f"   -> Set {motor_name} to {speed}")
                except ValueError:
                    print("   Invalid number.")

        except ValueError:
            print("Invalid input.")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    print("Cleaning up...")
    stop_all_motors()
    time.sleep(0.5)
    for pin in MOTORS:
        pi.set_servo_pulsewidth(pin, 0)
    pi.stop()