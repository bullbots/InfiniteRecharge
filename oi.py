from wpilib.joystick import Joystick
from wpilib.buttons import JoystickButton
from commands.spin_timed import SpinTimed
from commands.move_timed import MoveTimed
from commands.shooter_test import ShooterTest

class OI:

    def __init__(self):
        self.stick = Joystick(0)

        self.button1 = JoystickButton(self.stick, 1)
        self.button1.whileHeld(ShooterTest())
        self.button2 = JoystickButton(self.stick, 2)
        self.button2.whenPressed(SpinTimed(100))
