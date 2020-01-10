from wpilib.joystick import Joystick
from wpilib.buttons import JoystickButton
from commands.spin_timed import SpinTimed
from commands.move_timed import MoveTimed


class OI:

    def __init__(self):
        self.stick = Joystick(0)
