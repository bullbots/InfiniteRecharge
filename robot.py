import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot

from subsystems.drivetrain import DriveTrain
from subsystems.shooter import Shooter
from oi import OI
from commands.autonomus_driving import AutonomusDriving

from wpilib.smartdashboard import SmartDashboard
import math
import pathfinder as pf
from ctre._impl import ControlMode

import time


class InfiniteRechargeRobot(CommandBasedRobot):

    # Robot attributes
    WHEEL_DIAMETER = 0.5  # 6 inches
    ENCODER_COUNTS_PER_REV = 360

    # Pathfinder constants
    MAX_VELOCITY = 5  # ft/s
    MAX_ACCELERATION = 6

    def robotInit(self):
        """This code runs at robot start, initialize subsystems here."""
        super().robotInit()

        # Position gets automatically updated as robot moves
        self.gyro = wpilib.AnalogGyro(1)

        self.l_encoder = wpilib.Encoder(0, 1)
        self.l_encoder.setDistancePerPulse(
            (math.pi * self.WHEEL_DIAMETER) / self.ENCODER_COUNTS_PER_REV
        )

        self.r_encoder = wpilib.Encoder(2, 3)
        self.r_encoder.setDistancePerPulse(
            (math.pi * self.WHEEL_DIAMETER) / self.ENCODER_COUNTS_PER_REV
        )


        # Set up method to access robot anywhere
        Command.getRobot = lambda: self

        # Initialize Subsystems
        self.drivetrain = DriveTrain()
        self.shooter = Shooter()
        self.oi = OI()
        self.autonomousCommand = AutonomusDriving()

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
#        self.autonomousCommand.start()

# debug
        # capture the start time
        self.timeAutoStart = time.time()

# TESTING PATHFINDER
        # Set up the trajectory
        points = [pf.Waypoint(0, 0, 0), pf.Waypoint(9, 5, pf.d2r(90)), pf.Waypoint(18, 10, pf.d2r(-45))]

        info, trajectory = pf.generate(
            points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            dt=self.getPeriod(),
            max_velocity=self.MAX_VELOCITY,
            max_acceleration=self.MAX_ACCELERATION,
            max_jerk=120.0,
        )

        # Wheelbase Width = 2 ft
        modifier = pf.modifiers.TankModifier(trajectory).modify(2.0)

        # Do something with the new Trajectories...
        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        leftFollower = pf.followers.EncoderFollower(left)
        leftFollower.configureEncoder(
            self.l_encoder.get(), self.ENCODER_COUNTS_PER_REV, self.WHEEL_DIAMETER
        )
        leftFollower.configurePIDVA(1.0, 0.0, 0.0, 1 / self.MAX_VELOCITY, 0)

        rightFollower = pf.followers.EncoderFollower(right)
        rightFollower.configureEncoder(
            self.r_encoder.get(), self.ENCODER_COUNTS_PER_REV, self.WHEEL_DIAMETER
        )
        rightFollower.configurePIDVA(1.0, 0.0, 0.0, 1 / self.MAX_VELOCITY, 0)

        self.leftFollower = leftFollower
        self.rightFollower = rightFollower

        # This code renders the followed path on the field in simulation (requires pyfrc 2018.2.0+)
        if wpilib.RobotBase.isSimulation():
            from pyfrc.sim import get_user_renderer

            renderer = get_user_renderer()
            if renderer:
                renderer.draw_pathfinder_trajectory(
                    left, color="#0000ff", offset=(-1, 0)
                )
                renderer.draw_pathfinder_trajectory(
                    modifier.source, color="#00ff00", show_dt=1.0, dt_offset=0.0
                )
                renderer.draw_pathfinder_trajectory(
                    right, color="#0000ff", offset=(1, 0)
                )

    def autonomousPeriodic(self):
        """This code runs every 20ms when the robot is in autonomous mode"""
        super().autonomousPeriodic()

        l_encoder_val = self.l_encoder.get()
        r_encoder_val = self.l_encoder.get()
        can_l_encoder_val = self.drivetrain._left_master_talon.getSelectedSensorPosition()
        can_r_encoder_val = self.drivetrain._right_master_talon.getSelectedSensorPosition()

        l = self.leftFollower.calculate(l_encoder_val)
        r = self.rightFollower.calculate(r_encoder_val)

        # debug
        encoder_debug_output = "left encoder: {l_encoder_val}, right encoder: {r_encoder_val}, left CAN encoder: {can_l_encoder_val}, right CAN encoder: {can_r_encoder_val}"
        if self.isSimulation():
            self.logger.info(f"{encoder_debug_output}")
        else:
            SmartDashboard.putString("Encoder Debug", encoder_debug_output)

        gyro_heading = (
            -self.gyro.getAngle()
        )  # Assuming the gyro is giving a value in degrees
        desired_heading = pf.r2d(
            self.leftFollower.getHeading()
        )  # Should also be in degrees

        # This is a poor man's P controller
        angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
        turn = 5 * (-1.0 / 80.0) * angleDifference

        l = l + turn
        r = r - turn

        # -1 is forward, so invert both values
        # self.robot_drive.tankDrive(-l, -r)
        self.drivetrain.set(ControlMode.PercentOutput, l, r)

    def teleopInit(self):
        """This code runs when we start teleop mode"""
        super().teleopInit()

    def teleopPeriodic(self):
        """This code runs every 20ms when the robot is in teleop mode"""
        super().teleopPeriodic()


if __name__ == "__main__":
    wpilib.run(InfiniteRechargeRobot)
