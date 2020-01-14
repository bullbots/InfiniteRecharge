from wpilib.command.subsystem import Subsystem
from robotmap import RobotMap
from ctre.wpi_talonsrx import WPI_TalonSRX
from rev import CANSparkMax, MotorType
from constants import Constants
from ctre._impl import FeedbackDevice, ControlMode


class Shooter(Subsystem):
    def __init__(self):
        super().__init__()

        self.top_shooter = CANSparkMax(RobotMap.TOP_SHOOTER_SPARKMAX, MotorType.kBrushless)
        self.bottom_shooter = CANSparkMax(RobotMap.BOTTOM_SHOOTER_SPARKMAX, MotorType.kBrushless)

        self.top_shooter_encoder = self.top_shooter.getEncoder()

        self.top_shooter_pid = self.top_shooter.getPIDController()

        self.top_shooter_pid.setReference(0)

        self.top_shooter.getSelectedSensorVelocity(0)
        self.bottom_shooter.getSelectedSensorVelocity(0)
        self.configure_pid()

        self.top_shooter_velocity = self.top_shooter.getSelectedSensorVelocity(0)
        self.bottom_shooter_velocity = self.bottom_shooter.getSelectedSensorVelocity(0)

    def configure_pid(self):
        self.top_shooter.config_kF(0, Constants.SHOOTER_VELOCITY_F, Constants.TIMEOUT_MS)
        self.top_shooter.config_kP(0, Constants.SHOOTER_VELOCITY_P, Constants.TIMEOUT_MS)
        self.top_shooter.config_kI(0, Constants.SHOOTER_VELOCITY_I, Constants.TIMEOUT_MS)
        self.top_shooter.config_kD(0, Constants.SHOOTER_VELOCITY_D, Constants.TIMEOUT_MS)

        self.bottom_shooter.config_kF(0, Constants.SHOOTER_VELOCITY_F, Constants.TIMEOUT_MS)
        self.bottom_shooter.config_kP(0, Constants.SHOOTER_VELOCITY_P, Constants.TIMEOUT_MS)
        self.bottom_shooter.config_kI(0, Constants.SHOOTER_VELOCITY_I, Constants.TIMEOUT_MS)
        self.bottom_shooter.config_kD(0, Constants.SHOOTER_VELOCITY_D, Constants.TIMEOUT_MS)

    def motor_on(self):
        self.top_shooter.set(ControlMode.Velocity, Constants.SHOOTER_SPARKMAX_MAX_SPEED)

        self.bottom_shooter.set(ControlMode.Velocity, Constants.SHOOTER_SPARKMAX_MAX_SPEED)

    def motor_off(self):
        self.top_shooter.set(0)

        self.bottom_shooter.set(0)

    def set(self, control_mode: CANSparkMax.ControlMode, top_spin_magnitude, bottom_spin_magnitude):
        self.top_shooter.set(control_mode, top_spin_magnitude)

        self.bottom_shooter.set(control_mode, bottom_spin_magnitude)
