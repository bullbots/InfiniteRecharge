from wpilib.command.subsystem import Subsystem
from robotmap import RobotMap
from wpilib.drive.differentialdrive import DifferentialDrive

from commands.joystick_drive import JoystickDrive
from ctre.wpi_talonsrx import WPI_TalonSRX
import wpilib

class DriveTrain(Subsystem):
    def __init__(self):
        super().__init__()

        self.leftMasterTalon = WPI_TalonSRX(RobotMap.LEFT_MASTER_TALON)
        self.leftSlaveTalon = WPI_TalonSRX(RobotMap.LEFT_SLAVE_TALON)
        self.rightMasterTalon = WPI_TalonSRX(RobotMap.RIGHT_MASTER_TALON)
        self.rightSlaveTalon = WPI_TalonSRX(RobotMap.RIGHT_SLAVE_TALON)

        self.leftSlaveTalon.follow(self.leftMasterTalon)
        self.rightSlaveTalon.follow(self.rightMasterTalon)

        self.leftMasterTalon.setInverted(True)
        self.leftSlaveTalon.setInverted(True)

        self.drive = DifferentialDrive(self.leftMasterTalon, self.rightMasterTalon)

    def diffdrive(self, x, y):

        x = self.deadband(x)
        y = self.deadband(y)

        self.drive.arcadeDrive(x, y)

    def deadband(self, num):
        deadband_value = .1
        if deadband_value < num < deadband_value:
            num = 0
        return num

    def initDefaultCommand(self) -> None:
        self.setDefaultCommand(JoystickDrive())