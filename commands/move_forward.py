from wpilib.command import Command
from ctre._impl import ControlMode


class MoveForward(Command):
    def __init__(self, distance):
        super().__init__(subsystem=Command.getRobot().drivetrain)
        self.distance = distance

    def initialize(self):
        Command.getRobot().drivetrain.set(ControlMode.MotionMagic, self.distance, self.distance)

    def isFinished(self):
        left, right = Command.getRobot().drivetrain.getPosition()
        left_error = abs(self.distance - left)
        right_error = abs(self.distance - right)
        return left_error < 400 and right_error < 400

    def end(self):
        Command.getRobot().drivetrain.set(ControlMode.PercentOutput, 0, 0)