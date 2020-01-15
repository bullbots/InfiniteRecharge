from wpilib.command import Command
from ctre._impl import ControlMode
from constants import Constants
from subsystems.shooter import Shooter

from wpilib.smartdashboard import SmartDashboard


class ShooterTest(Command):
    def __init__(self):
        super().__init__(subsystem=Command.getRobot().shooter, name="Shooter")

        self.integral = 0
        self.previous_error = 0

        self.start_speed = 0
        self.goal_speed = Constants.SHOOTER_SPEED_PERCENT_OUTPUT
        self.top_motor_current_speed = Command.getRobot().shooter.top_shooter_velocity
        self.bottom_motor_current_speed = Command.getRobot().shooter.bottom_shooter_velocity

        top_error = self.goal_speed - self.top_motor_current_speed
        bottom_error = self.goal_speed - self.bottom_motor_current_speed
        self.top_integral = self.integral + top_error
        self.bottom_integral = self.integral + bottom_error
        self.top_derivative = (top_error - self.previous_error)
        self.bottom_derivative = (bottom_error - self.previous_error)
        self.top_output = Constants.SHOOTER_VELOCITY_P * top_error + Constants.SHOOTER_VELOCITY_I * self.top_integral + Constants.SHOOTER_VELOCITY_D * self.top_derivative
        self.bottom_output = Constants.SHOOTER_VELOCITY_P * bottom_error + Constants.SHOOTER_VELOCITY_I * self.bottom_integral + Constants.SHOOTER_VELOCITY_D * self.bottom_derivative

        SmartDashboard.putBoolean("Shooter On/Off", False)

    def execute(self):
        Command.getRobot().shooter.set(self.top_output, self.bottom_output)

        SmartDashboard.putBoolean("Shooter On/Off", True)
        SmartDashboard.putNumber("Top Motor Current Speed", self.top_motor_current_speed)
        SmartDashboard.putNumber("Bottom Motor Current Speed", self.bottom_motor_current_speed)

    def end(self):
        Command.getRobot().shooter.motor_off()

        SmartDashboard.putBoolean("Shooter On/Off", False)
