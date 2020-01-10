from wpilib.joystick import Joystick
from wpilib.buttons import JoystickButton
from commands.spin_timed import SpinTimed


class OI:

    def __init__(self):
        self.stick = Joystick(0)
        self.buttonone = JoystickButton(self.stick, 1)
        self.buttonone.whenPressed(SpinTimed(3))