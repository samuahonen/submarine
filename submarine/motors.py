import RPi.GPIO as GPIO
import time

# UP and DOWN motors
LiftMotor_1 = 12  
LiftMotor_2 = 12 
LiftMotor_3 = 12 

# Forwqard and Backward motors
DriveMotor_1 = 18  
DriveMotor_2 = 23

class ESC:
    pass



class MotorsController:
    def set_throttle(self, ms, pwm):
        duty = (ms / 20.0) * 100.0
        pwm.ChangeDutyCycle(duty)
        print(f"Throttle set to {ms:.2f} ms ({duty:.1f}% duty)")
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DriveMotor_1, GPIO.OUT)
        GPIO.setup(DriveMotor_2, GPIO.OUT)
        self.pwm_left = GPIO.PWM(DriveMotor_1, 50)
        self.pwm_left.start(0)
        self.pwm_right = GPIO.PWM(DriveMotor_2, 50)
        self.pwm_right.start(0)
        print("MotorsController initialized.")

    def lift_up(self):
        pass 
    
    def lift_down(self):
        pass
    
    def lift_stop(self):
        pass
    
    def forward(self):
        self.set_throttle(1.5, self.pwm_left)
        self.set_throttle(1.5, self.pwm_right)
        time.sleep(0.3) 

        self.set_throttle(2.0, self.pwm_left)
        time.sleep(0.05)
        self.set_throttle(2.0, self.pwm_right)
        print("Moving forward...")

    
    def backward(self):
        pass
    
    def stop(self):
        self.set_throttle(0.0, self.pwm_left)
        self.set_throttle(0.0, self.pwm_right)
        #GPIO.cleanup()

    def right(self):
        self.set_throttle(2.0, self.pwm_left)
        self.set_throttle(1.0, self.pwm_right)

    def left(self):
        self.set_throttle(1.0, self.pwm_left)
        self.set_throttle(2.0, self.pwm_right)
