from wpilib.command import TimedCommand
from wpilib.command import Command
from ctre._impl import ControlMode
from wpilib.smartdashboard import SmartDashboard


class SpinTimed(TimedCommand):

    def __init__(self, duration):
        super().__init__(subsystem=Command.getRobot().drivetrain, timeoutInSeconds=duration, name="SpinTimed")

    def initialize(self):
        SmartDashboard.putBoolean("Spin Timed On/Off", True)

    def execute(self):
        Command.getRobot().drivetrain.set(ControlMode.PercentOutput, 1, -1)

    def end(self):
        Command.getRobot().drivetrain.stop()

        SmartDashboard.putBoolean("Spin Timed On/Off", False)