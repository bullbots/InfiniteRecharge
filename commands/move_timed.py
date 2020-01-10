from wpilib.command import TimedCommand
from wpilib.command import Command
from ctre._impl import ControlMode


class MoveTimed(TimedCommand):
    def __init__(self, duration):
        super().__init__(subsystem=Command.getRobot().drivetrain, timeoutInSeconds=duration, name="MoveTimed")
    
    def execute(self):
        Command.getRobot().drivetrain.set(ControlMode.PercentOutput, 1, 1)

    def end(self):
        Command.getRobot().drivetrain.stop()