import wpilib


from wpilib.command import Command
from commandbased import CommandBasedRobot

from subsystems.drivetrain import DriveTrain

from oi import OI


class InfiniteRechargeRobot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda: self
        self.drivetrain = DriveTrain()
        self.oi = OI()


if __name__ == "__main__":
    wpilib.run(InfiniteRechargeRobot)
