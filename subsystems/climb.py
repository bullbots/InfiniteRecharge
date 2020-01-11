from wpilib.command.subsystem import Subsystem
from ctre.wpi_talonsrx import WPI_TalonSRX
from robotmap import RobotMap


class Climb(Subsystem):

    def __init__(self):
        super().__init__()

        self._climb_talon = WPI_TalonSRX(RobotMap.CLIMB_TALON)