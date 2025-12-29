import pigpio
import time

# --- CONFIGURATION ---
# Connect to pigpio daemon
pi = pigpio.pi()

# Check connection immediately
if not pi.connected:
    print("ERROR: Pigpio daemon is not running. Please run: sudo pigpiod")
    exit()

# Pin Definitions
LiftMotor_CENTER = 16
LiftMotor_LEFT   = 20
LiftMotor_RIGHT  = 21

DriveMotor_LEFT  = 23
DriveMotor_RIGHT = 24

# Speed Settings (Tune these numbers!)
# usually: 1500=Stop, >1500=Forward, <1500=Reverse
SPEED_LIFT_UP   = 1600
SPEED_LIFT_DOWN = 1400

SPEED_DRIVE_FWD = 1600
SPEED_DRIVE_REV = 1400

class ESC:
    def __init__(self, pin, neutral_point):
        self.pin = pin
        self.neutral_point = neutral_point
        
        # Initialize the ESC
        print(f"Initializing Pin {self.pin} at {self.neutral_point}us")
        pi.set_servo_pulsewidth(self.pin, self.neutral_point)
        time.sleep(1) # Wait for ESC to arm
    
    def set_pulse(self, microseconds):
        """Sets the raw pulse width in microseconds."""
        # Safety hard limits
        if microseconds < 1000: microseconds = 1000
        if microseconds > 2000: microseconds = 2000
        
        pi.set_servo_pulsewidth(self.pin, microseconds)
    
    def neutral(self):
        """Stops the motor using its specific neutral point."""
        self.set_pulse(self.neutral_point)

    def stop_signal(self):
        """Stops the PWM signal entirely (electrical off)."""
        pi.set_servo_pulsewidth(self.pin, 0)

class MotorsController:    
    def __init__(self):
        print("Starting Motor Controller...")
        
        # Initialize Lift Motors (Note: Left/Right use 1480, Center uses 1500)
        self.lift_left   = ESC(LiftMotor_LEFT, neutral_point=1480)
        self.lift_right  = ESC(LiftMotor_RIGHT, neutral_point=1480)
        self.lift_center = ESC(LiftMotor_CENTER, neutral_point=1500)
        
        # Initialize Drive Motors (Standard 1500)
        self.drive_left  = ESC(DriveMotor_LEFT, neutral_point=1500)
        self.drive_right = ESC(DriveMotor_RIGHT, neutral_point=1500)
        
        # Ensure everything is stopped/armed on startup
        self.stop()
        print("Motors Armed and Ready.")
        time.sleep(2) 

    # --- LIFT CONTROLS ---
    def lift_up(self):
        self.lift_left.set_pulse(SPEED_LIFT_UP)
        self.lift_right.set_pulse(SPEED_LIFT_UP)
        self.lift_center.set_pulse(SPEED_LIFT_UP)
    
    def lift_down(self):
        self.lift_left.set_pulse(SPEED_LIFT_DOWN)
        self.lift_right.set_pulse(SPEED_LIFT_DOWN)
        self.lift_center.set_pulse(SPEED_LIFT_DOWN)
    
    def lift_stop(self):
        self.lift_left.neutral()
        self.lift_right.neutral()
        self.lift_center.neutral()
    
    # --- DRIVE CONTROLS ---
    def forward(self):
        self.drive_left.set_pulse(SPEED_DRIVE_FWD)
        self.drive_right.set_pulse(SPEED_DRIVE_FWD)
    
    def backward(self):
        self.drive_left.set_pulse(SPEED_DRIVE_REV)
        self.drive_right.set_pulse(SPEED_DRIVE_REV)
    
    def left(self):
        # Tank turn: Left back, Right forward
        self.drive_left.set_pulse(SPEED_DRIVE_REV) 
        self.drive_right.set_pulse(SPEED_DRIVE_FWD) 

    def right(self):
        # Tank turn: Left forward, Right back
        self.drive_left.set_pulse(SPEED_DRIVE_FWD) 
        self.drive_right.set_pulse(SPEED_DRIVE_REV) 
    
    def stop(self):
        self.drive_left.neutral()
        self.drive_right.neutral()
        self.lift_stop()
        
    def cleanup(self):
        print("Cleaning up...")
        self.stop()
        time.sleep(0.5)
        
        # Kill signals
        self.drive_left.stop_signal()
        self.drive_right.stop_signal()
        self.lift_center.stop_signal()
        self.lift_left.stop_signal()
        self.lift_right.stop_signal()
        
        # Stop pigpio
        pi.stop()

# --- EXAMPLE USAGE IF RUN DIRECTLY ---
if __name__ == "__main__":
    try:
        controller = MotorsController()
        
        print("Testing Lift Up...")
        controller.lift_up()
        time.sleep(2)
        
        print("Testing Lift Stop...")
        controller.lift_stop()
        time.sleep(1)
        
        print("Testing Drive Forward...")
        controller.forward()
        time.sleep(2)
        
        print("Stopping...")
        controller.stop()

    except KeyboardInterrupt:
        print("\nExiting...")
    
    finally:
        # If controller was created, clean it up
        if 'controller' in locals():
            controller.cleanup()