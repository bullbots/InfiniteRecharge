from wpilib.command.subsystem import Subsystem
from robotmap import RobotMap
from ctre.wpi_talonsrx import WPI_TalonSRX


class Shooter(Subsystem):
    def __init__(self):
        super().__init__()

        self.shooterTalon = WPI_TalonSRX(RobotMap.SHOOTER_TALON)
