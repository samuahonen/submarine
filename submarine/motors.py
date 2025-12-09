import RPi.GPIO as GPIO
import time

# UP and DOWN motors
LiftMotor_CENTER = 16
LiftMotor_LEFT = 20
LiftMotor_RIGHT = 21

# Forward and Backward motors
DriveMotor_LEFT = 23
DriveMotor_RIGHT = 24

# ESC pulse width range (microseconds)
MIN_PULSE = 1000
NEUTRAL_PULSE = 1500
MAX_PULSE = 2000


class ESC:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz frequency
        self.pwm.start(0)
    
    def set_speed(self, microseconds):
        """Set ESC speed using pulse width in microseconds (1000-2000)."""
        duty = (microseconds / 20000) * 100
        self.pwm.ChangeDutyCycle(duty)
    
    def neutral(self):
        """Set ESC to neutral/stopped position."""
        self.set_speed(NEUTRAL_PULSE)

    def stop(self):
        self.pwm.stop()


class MotorsController:    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
        print("Initializing motors...")
        self.drive_left = ESC(DriveMotor_LEFT)
        self.drive_right = ESC(DriveMotor_RIGHT)
        self.lift_center = ESC(LiftMotor_CENTER)
        self.lift_left = ESC(LiftMotor_LEFT)
        self.lift_right = ESC(LiftMotor_RIGHT)
        
        # Initialize all ESCs to neutral for 3 seconds
        print("Arming ESCs (sending neutral signal)...")
        self.drive_left.neutral()
        self.drive_right.neutral()
        self.lift_center.neutral()
        self.lift_left.neutral()
        self.lift_right.neutral()
        time.sleep(3)
        
        print("MotorsController ready!")

    def lift_up(self):
        """Lift motors forward (up)."""
        self.lift_center.set_speed(1600)
        self.lift_left.set_speed(1600)
        self.lift_right.set_speed(1600)
    
    def lift_down(self):
        """Lift motors reverse (down)."""
        self.lift_center.set_speed(1400)
        self.lift_left.set_speed(1400)
        self.lift_right.set_speed(1400)
    
    def lift_stop(self):
        """Stop lift motors."""
        self.lift_center.neutral()
        self.lift_left.neutral()
        self.lift_right.neutral()
    
    def forward(self):
        """Drive forward."""
        self.drive_left.set_speed(1600)
        self.drive_right.set_speed(1600)
    
    def backward(self):
        """Drive backward."""
        self.drive_left.set_speed(1400)
        self.drive_right.set_speed(1400)
    
    def left(self):
        self.drive_left.set_speed(1500)
        self.drive_right.set_speed(1600)

    def right(self):
        self.drive_left.set_speed(1600)
        self.drive_right.set_speed(1500)
    
    def stop(self):
        """Stop drive motors."""
        self.drive_left.neutral()
        self.drive_right.neutral()
        self.lift_center.neutral()
        self.lift_left.neutral()
        self.lift_right.neutral()
        
    def cleanup(self):
        """Return all motors to neutral and cleanup GPIO."""
        print("Stopping all motors...")
        self.drive_left.neutral()
        self.drive_right.neutral()
        self.lift_center.neutral()
        self.lift_left.neutral()
        self.lift_right.neutral()
        time.sleep(0.5)
        
        self.drive_left.stop()
        self.drive_right.stop()
        self.lift_center.stop()
        self.lift_left.stop()
        self.lift_right.stop()
        GPIO.cleanup()
        print("MotorsController cleaned up.")