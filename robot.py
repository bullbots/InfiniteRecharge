import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot

from subsystems.drivetrain import DriveTrain
from subsystems.shooter import Shooter
from oi import OI


class InfiniteRechargeRobot(CommandBasedRobot):

    def robotInit(self):
        """This code runs at robot start, initialize subsystems here."""
        super().robotInit()

        # Set up method to access robot anywhere
        Command.getRobot = lambda: self

        # Initialize Subsystems
        self.drivetrain = DriveTrain()
        self.shooter = Shooter()
        self.oi = OI()

    def robotPeriodic(self):
        """This code runs every 20ms regardless of robot state"""
        super().robotPeriodic()

    def disabledInit(self):
        """This code runs when we disable the robot."""
        super().disabledInit()
        self.drivetrain.stop()

    def disabledPeriodic(self):
        """This code runs every 20ms when the robot is disabled."""
        super().disabledPeriodic()
        Command.getRobot().drivetrain.diffdrive(0, 0)

    def autonomousInit(self):
        """This code runs when we start autonomous mode"""
        super().autonomousInit()

    def autonomousPeriodic(self):
        """This code runs every 20ms when the robot is in autonomous mode"""
        super().autonomousPeriodic()

    def teleopInit(self):
        """This code runs when we start teleop mode"""
        super().teleopInit()

    def teleopPeriodic(self):
        """This code runs every 20ms when the robot is in teleop mode"""
        super().teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(InfiniteRechargeRobot)
