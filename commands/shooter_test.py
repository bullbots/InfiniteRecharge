from wpilib.command import Command
from ctre._impl import ControlMode

from wpilib.smartdashboard import SmartDashboard


class ShooterTest(Command):
    def __init__(self):
        super().__init__(subsystem=Command.getRobot().shooter, name="Shooter")

        SmartDashboard.putBoolean("Shooter On/Off", False)

    def initialize(self):
        Command.getRobot().shooter.set(ControlMode.PercentOutput, .5)

        SmartDashboard.putBoolean("Shooter On/Off", True)

    def end(self):
        Command.getRobot().shooter.motor_off()

        SmartDashboard.putBoolean("Shooter On/Off", False)
