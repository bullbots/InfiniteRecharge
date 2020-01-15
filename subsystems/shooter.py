from wpilib.command.subsystem import Subsystem
from robotmap import RobotMap
from ctre.wpi_talonsrx import WPI_TalonSRX
from rev import CANSparkMax, MotorType, ControlType
from constants import Constants


class Shooter(Subsystem):
    def __init__(self):
        super().__init__()

        self.top_shooter = CANSparkMax(RobotMap.TOP_SHOOTER_SPARKMAX, MotorType.kBrushless)
        self.bottom_shooter = CANSparkMax(RobotMap.BOTTOM_SHOOTER_SPARKMAX, MotorType.kBrushless)

        self.top_shooter_encoder = self.top_shooter.getEncoder()
        self.bottom_shooter_encoder = self.bottom_shooter.getEncoder()

        self.top_shooter_velocity = self.top_shooter_encoder.getVelocity()
        self.bottom_shooter_velocity = self.bottom_shooter_encoder.getVelocity()

        self.top_shooter_pid = self.top_shooter.getPIDController()
        self.bottom_shooter_pid = self.bottom_shooter.getPIDController()

        self.top_shooter_pid.setReference(0, ControlType.kSmartVelocity)
        self.bottom_shooter_pid.setReference(0, ControlType.kSmartVelocity)

        self.configure_pid()

    def configure_pid(self):
        self.top_shooter_pid.setFF(Constants.SHOOTER_VELOCITY_F)
        self.top_shooter_pid.setP(Constants.SHOOTER_VELOCITY_P)
        self.top_shooter_pid.setI(Constants.SHOOTER_VELOCITY_I)
        self.top_shooter_pid.setD(Constants.SHOOTER_VELOCITY_D)

        self.bottom_shooter_pid.setFF(Constants.SHOOTER_VELOCITY_F)
        self.bottom_shooter_pid.setP(Constants.SHOOTER_VELOCITY_P)
        self.bottom_shooter_pid.setI(Constants.SHOOTER_VELOCITY_I)
        self.bottom_shooter_pid.setD(Constants.SHOOTER_VELOCITY_D)

    def motor_on(self):
        self.top_shooter.set(Constants.SHOOTER_SPARKMAX_MAX_SPEED)

        self.bottom_shooter.set(Constants.SHOOTER_SPARKMAX_MAX_SPEED)

    def motor_off(self):
        self.top_shooter.set(0)

        self.bottom_shooter.set(0)

    def set(self, top_spin_magnitude, bottom_spin_magnitude):
        self.top_shooter.set(top_spin_magnitude)

        self.bottom_shooter.set(bottom_spin_magnitude)
