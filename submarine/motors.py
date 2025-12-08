import RPi.GPIO as GPIO
import time

# UP and DOWN motors
LiftMotor_CENTER = 16  #CENTER
LiftMotor_LEFT = 20  #LEFT
LiftMotor_RIGHT = 21  #RIGHT

# Forward and Backward motors
DriveMotor_LEFT = 23  #LEFT
DriveMotor_RIGHT = 24  #RIGHT

class ESC:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz frequency
        self.pwm.start(0)  # Start with 0% duty cycle
    
    def set_speed(self, microseconds):
        duty = (microseconds / 20000) * 100
        self.pwm.ChangeDutyCycle(duty)

    def stop(self):
        self.pwm.stop()

    def cleanup(self):
        GPIO.cleanup()



class MotorsController:    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.drive_left = ESC(DriveMotor_LEFT)
        self.drive_right = ESC(DriveMotor_RIGHT)
        self.lift_center = ESC(LiftMotor_CENTER)
        self.lift_left = ESC(LiftMotor_LEFT)
        self.lift_right = ESC(LiftMotor_RIGHT)
        print("MotorsController initialized.")

    def lift_up(self):
        self.lift_center.set_speed(2.0)
        self.lift_left.set_speed(2.0)
        self.lift_right.set_speed(2.0)
        print("Lifting up...") 
    
    def lift_down(self):
        self.lift_center.set_speed(1.0)
        self.lift_left.set_speed(1.0)
        self.lift_right.set_speed(1.0)
        print("Lifting down...")
    
    def lift_stop(self):
        self.lift_center.set_speed(0.0)
        self.lift_left.set_speed(0.0)
        self.lift_right.set_speed(0.0)
        print("Lift stopped.")
    
    def forward(self):
        self.drive_left.set_speed(1.5)
        self.drive_right.set_speed(1.5)
        time.sleep(0.3) 

        self.drive_left.set_speed(2.0)
        time.sleep(0.05)
        self.drive_right.set_speed(2.0)
        print("Moving forward...")

    
    def backward(self):
        self.drive_left.set_speed(1.0)
        self.drive_right.set_speed(1.0)
        time.sleep(0.3) 

        self.drive_left.set_speed(0.0)
        time.sleep(0.05)
        self.drive_right.set_speed(0.0)
        print("Moving backward...")
    
    def stop(self):
        self.drive_left.set_speed(0.0)
        self.drive_right.set_speed(0.0)

    def right(self):
        self.drive_left.set_speed(2.0)
        self.drive_right.set_speed(1.0)

    def left(self):
        self.drive_left.set_speed(1.0)
        self.drive_right.set_speed(2.0)
        
    def cleanup(self):
        self.drive_left.stop()
        self.drive_right.stop()
        self.lift_center.stop()
        self.lift_left.stop()
        self.lift_right.stop()
        GPIO.cleanup()
        print("MotorsController cleaned up.")