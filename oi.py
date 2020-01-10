from wpilib.joystick import Joystick
from wpilib.buttons import JoystickButton
from commands.move_timed import MoveTimed

class OI:

    def __init__(self):
        self.stick = Joystick(0)
        self.button1 = JoystickButton(self.stick, 1)
        self.button1.whenPressed(MoveTimed(3))
