from wpilib.command.subsystem import Subsystem
from robotmap import RobotMap
from wpilib.drive.differentialdrive import DifferentialDrive

from commands.joystick_drive import JoystickDrive
from ctre.wpi_talonsrx import WPI_TalonSRX
from constants import Constants
from drive_interpreter import DriveHelper
from wpilib.smartdashboard import SmartDashboard


class DriveTrain(Subsystem):
    def __init__(self):
        super().__init__()

        # Create our motor controllers
        self._left_master_talon = WPI_TalonSRX(RobotMap.LEFT_MASTER_TALON)
        self._left_slave_talon = WPI_TalonSRX(RobotMap.LEFT_SLAVE_TALON)
        self._right_master_talon = WPI_TalonSRX(RobotMap.RIGHT_MASTER_TALON)
        self._right_slave_talon = WPI_TalonSRX(RobotMap.RIGHT_SLAVE_TALON)

        # Each side uses two motors, so we set one to follow the other
        self._left_slave_talon.follow(self._left_master_talon)
        self._right_slave_talon.follow(self._right_master_talon)

        # Left side is a mirror image, so invert the motor directions
        self._left_master_talon.setInverted(True)
        self._left_slave_talon.setInverted(True)

        # DifferentialDrive which conversts our joystick input to motor output, see diffdrive method
        self.drive = DifferentialDrive(self._left_master_talon, self._right_master_talon)

        # Drive Interpreter to convert joystick input to motor signal
        self.driveInterpreter = DriveHelper()

    def configure_pid(self):
        """Set all relevant PID Constants for the Drivetrain subsystem"""
        self._left_master_talon.config_kF(0, Constants.DRIVETRAIN_F)
        self._left_master_talon.config_kP(0, Constants.DRIVETRAIN_P)
        self._left_master_talon.config_kI(0, Constants.DRIVETRAIN_I)
        self._left_master_talon.config_kD(0, Constants.DRIVETRAIN_D)

        self._right_master_talon.config_kF(0, Constants.DRIVETRAIN_F)
        self._right_master_talon.config_kP(0, Constants.DRIVETRAIN_P)
        self._right_master_talon.config_kI(0, Constants.DRIVETRAIN_I)
        self._right_master_talon.config_kD(0, Constants.DRIVETRAIN_D)

    def diffdrive(self, x: float, y: float):
        """Maps Joystick input to motor output
        Args:
            x (float): X component of joystick input
            y (float): Y component of joystick input
        """
        x = self.deadband(x)
        y = self.deadband(y)

        self.drive.arcadeDrive(x, y, squareInputs=True)

        SmartDashboard.putNumber("left master voltage", self._left_master_talon.getMotorOutputVoltage())
        SmartDashboard.putNumber("right master voltage", self._right_master_talon.getMotorOutputVoltage())

    # This is experimental code
    def interpreted_drive(self, x: float, y: float):
        left_pwm, right_pwm = self.driveInterpreter.DriveSignal(y, x, False, False)
        self._left_master_talon.set(left_pwm)
        self._right_master_talon.set(right_pwm)

    def deadband(self, num):
        """Limit the allowed values from the joystick to be larger than .1"""
        deadband_value = .1
        if -deadband_value < num < deadband_value:
            num = 0
        return num

    def initDefaultCommand(self) -> None:
        self.setDefaultCommand(JoystickDrive())

    def set(self, control_mode: WPI_TalonSRX.ControlMode, left_magnitude: float, right_magnitude: float):
        """Sets Drivetrain control mode and magnitudes for left and right side

        Args:
            control_mode (WPI_TalonSRX.ControlMode): Control Mode for both motor controllers
            left_magnitude (float): Magnitude for the left side
            right_magnitude (float): Magnitude for the right side
        """
        self._left_master_talon.set(control_mode, left_magnitude)
        self._right_master_talon.set(control_mode, right_magnitude)

    def stop(self):
        """Sets all motor outputs to zero, run when robot is disabled"""
        self._left_master_talon.set(0)
        self._right_master_talon.set(0)
