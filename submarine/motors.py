import RPi.GPIO as GPIO
import time

LiftMotor_CENTER = 16
LiftMotor_LEFT = 20
LiftMotor_RIGHT = 21

DriveMotor_LEFT = 23
DriveMotor_RIGHT = 24

NEUTRAL_CAR = 1500
NEUTRAL_DRONE = 1000

class ESC:
    def __init__(self, pin, neutral_point):
        self.pin = pin
        self.neutral_point = neutral_point
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)
    
    def set_speed(self, microseconds):
        duty = (microseconds / 20000) * 100
        self.pwm.ChangeDutyCycle(duty)
    
    def neutral(self):
        self.set_speed(self.neutral_point)

    def stop(self):
        self.pwm.stop()

class MotorsController:    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        
        self.lift_left = ESC(LiftMotor_LEFT, NEUTRAL_CAR)
        self.lift_right = ESC(LiftMotor_RIGHT, NEUTRAL_CAR)
        
        self.drive_left = ESC(DriveMotor_LEFT, NEUTRAL_DRONE)
        self.drive_right = ESC(DriveMotor_RIGHT, NEUTRAL_DRONE)
        self.lift_center = ESC(LiftMotor_CENTER, NEUTRAL_DRONE)
        
        self.lift_left.neutral()
        self.lift_right.neutral()
        self.drive_left.neutral()
        self.drive_right.neutral()
        self.lift_center.neutral()
        
        time.sleep(3)

    def lift_up(self):
        self.lift_left.set_speed(1600)
        self.lift_right.set_speed(1600)
        self.lift_center.set_speed(1200)
    
    def lift_down(self):
        self.lift_left.set_speed(1400)
        self.lift_right.set_speed(1400)
        self.lift_center.set_speed(1000)
    
    def lift_stop(self):
        self.lift_left.neutral()
        self.lift_right.neutral()
        self.lift_center.neutral()
    
    def forward(self):
        self.drive_left.set_speed(1200)
        self.drive_right.set_speed(1200)
    
    def backward(self):
        self.drive_left.set_speed(1000)
        self.drive_right.set_speed(1000)
    
    def left(self):
        self.drive_left.set_speed(1000)
        self.drive_right.set_speed(1200)

    def right(self):
        self.drive_left.set_speed(1200)
        self.drive_right.set_speed(1000)
    
    def stop(self):
        self.drive_left.neutral()
        self.drive_right.neutral()
        self.lift_stop()
        
    def cleanup(self):
        self.stop()
        time.sleep(0.5)
        
        self.drive_left.stop()
        self.drive_right.stop()
        self.lift_center.stop()
        self.lift_left.stop()
        self.lift_right.stop()
        GPIO.cleanup()