import wpilib

from wpilib.command import Command
from commandbased import CommandBasedRobot

from oi import OI


class InfiniteRechargeRobot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda: self

        self.oi = OI()


if __name__ == "__main__":
    wpilib.run(InfiniteRechargeRobot)
