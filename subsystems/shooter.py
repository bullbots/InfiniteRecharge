from wpilib.command.subsystem import Subsystem
from robotmap import RobotMap
from ctre.wpi_talonsrx import WPI_TalonSRX
from constants import Constants
from ctre._impl import FeedbackDevice, ControlMode
from subsystems import drivetrain

class Shooter(Subsystem):
    def __init__(self):
        super().__init__()

        self.top_shooter_talon = WPI_TalonSRX(RobotMap.TOP_SHOOTER_TALON)
        self.bottom_shooter_talon = WPI_TalonSRX(RobotMap.BOTTOM_SHOOTER_TALON)

        self.top_shooter_talon.configSelectedFeedbackSensor(
            FeedbackDevice.CTRE_MagEncoder_Relative, 0, Constants.TIMEOUT_MS
        )
        self.top_shooter_talon.configSelectedFeedbackSensor(
            FeedbackDevice.CTRE_MagEncoder_Relative, 0, Constants.TIMEOUT_MS
        )
        
        self.configure_pid()

    def configure_pid(self):
        self.top_shooter_talon.config_kF(0, Constants.SHOOTER_VELOCITY_F, Constants.TIMEOUT_MS)
        self.top_shooter_talon.config_kP(0, Constants.SHOOTER_VELOCITY_P, Constants.TIMEOUT_MS)
        self.top_shooter_talon.config_kI(0, Constants.SHOOTER_VELOCITY_I, Constants.TIMEOUT_MS)
        self.top_shooter_talon.config_kD(0, Constants.SHOOTER_VELOCITY_D, Constants.TIMEOUT_MS)

        self.bottom_shooter_talon.config_kF(0, Constants.SHOOTER_VELOCITY_F, Constants.TIMEOUT_MS)
        self.bottom_shooter_talon.config_kP(0, Constants.SHOOTER_VELOCITY_P, Constants.TIMEOUT_MS)
        self.bottom_shooter_talon.config_kI(0, Constants.SHOOTER_VELOCITY_I, Constants.TIMEOUT_MS)
        self.bottom_shooter_talon.config_kD(0, Constants.SHOOTER_VELOCITY_D, Constants.TIMEOUT_MS)

    def motor_on(self):
        self.top_shooter_talon.set(ControlMode.Velocity, Constants.SHOOTER_TALON_MAX_SPEED)

        self.bottom_shooter_talon.set(ControlMode.Velocity, Constants.SHOOTER_TALON_MAX_SPEED)

    def motor_off(self):
        self.top_shooter_talon.set(0)

        self.bottom_shooter_talon.set(0)

    def set(self, control_mode: WPI_TalonSRX.ControlMode, spin_magnitude):
        self.top_shooter_talon.set(control_mode, spin_magnitude)

        self.bottom_shooter_talon.set(control_mode, spin_magnitude)