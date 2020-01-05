import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot

from subsystems.drivetrain import DriveTrain
from oi import OI


class InfiniteRechargeRobot(CommandBasedRobot):

    def robotInit(self):
        """This code runs when we start the robot, initialize subsystems here."""
        Command.getRobot = lambda: self
        self.drivetrain = DriveTrain()
        self.oi = OI()

    def robotPeriodic(self):
        """This code runs every 20ms regardless of robot state, usefull for logging code."""
        pass

    def disabledInit(self):
        """This code runs when we disable the robot."""
        pass

    def disabledPeriodic(self):
        """This code runs every 20ms when the robot is disabled."""
        pass

    def autonomousInit(self):
        """This code runs when we start autonomous mode"""
        pass

    def autonomousPeriodic(self):
        """This code runs every 20ms when the robot is in autonomous mode"""

    def teleopInit(self):
        """This code runs when we start teleop mode"""
        pass

    def teleopPeriodic(self):
        """This code runs every 20ms when the robot is in teleop mode"""
        pass


if __name__ == "__main__":
    wpilib.run(InfiniteRechargeRobot)
