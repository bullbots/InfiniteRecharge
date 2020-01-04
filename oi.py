from wpilib.joystick import Joystick

class OI(object):

    def __init__(self):
        self.stick = Joystick(0)
