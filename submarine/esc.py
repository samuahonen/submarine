

# UP and DOWN motors
LiftMotor_1 = 12  
LiftMotor_2 = 12 
LiftMotor_3 = 12 

# Forwqard and Backward motors
DriveMotor_1 = 12  
DriveMotor_2 = 12

class ESC:
    pass


class MotorsController:
    # Motor speed settings
    LIFT_UP_SPEED = 0.6
    LIFT_DOWN_SPEED = -0.6
    DRIVE_FORWARD_SPEED = 0.5
    DRIVE_BACKWARD_SPEED = -0.5

    # Motor stop settings
    LIFT_STOP = 0.0
    DRIVE_STOP = 0.0
    
    def __init__(self):
        pass    
    
    def lift_up(self):
        pass 
    
    def lift_down(self):
        pass
    
    def lift_stop(self):
        pass
    
    def forward(self):
        pass
    
    def backward(self):
        pass
    
    def stop(self):
        pass

    def right(self):
        pass

    def left(self):
        pass
