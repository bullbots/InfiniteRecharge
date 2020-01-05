from wpilib.command.subsystem import Subsystem
from robotmap import RobotMap
from ctre.wpi_talonsrx import WPI_TalonSRX
from constants import Constants
from ctre._impl import FeedbackDevice, ControlMode


class Shooter(Subsystem):
    def __init__(self):
        super().__init__()

        self.shooterTalon = WPI_TalonSRX(RobotMap.SHOOTER_TALON)

        self.shooterTalon.configSelectedFeedbackSensor(FeedbackDevice.CTRE_MagEncoder_Relative, 0,
                                                       Constants.TIMEOUT_MS)
        self.configure_pid()

    def configure_pid(self):
        self.shooterTalon.config_kF(0, Constants.SHOOTER_VELOCITY_F, Constants.TIMEOUT_MS)
        self.shooterTalon.config_kP(0, Constants.SHOOTER_VELOCITY_P, Constants.TIMEOUT_MS)
        self.shooterTalon.config_kI(0, Constants.SHOOTER_VELOCITY_I, Constants.TIMEOUT_MS)
        self.shooterTalon.config_kD(0, Constants.SHOOTER_VELOCITY_D, Constants.TIMEOUT_MS)

    def motor_on(self):
        self.shooterTalon.set(WPI_TalonSRX.ControlMode.Velocity, Constants.SHOOTER_TALON_MAX_SPEED)

    def motor_off(self):
        self.shooterTalon.set(0)
