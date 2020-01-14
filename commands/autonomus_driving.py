from wpilib.command import CommandGroup, WaitCommand

from commands.move_timed import MoveTimed
from commands.spin_timed import SpinTimed
import pathfinder as pf
import constants
from subsystems.drivetrain import DriveTrain

class AutonomusDriving(CommandGroup):

    # Pathfinder constants
    MAX_VELOCITY = 5  # ft/s
    MAX_ACCELERATION = 6


    def __init__(self):
        super().__init__()

        points = [pf.Waypoint(0, 0, 0), pf.Waypoint(9, 5, 0)]

        info, trajectory = pf.generate(
            points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            dt=constants.Constants.GETPERIODPATHFINDER,
            max_velocity=self.MAX_VELOCITY,
            max_acceleration=self.MAX_ACCELERATION,
            max_jerk=120.0,
        )

        def autonomousPeriodic(self):
            l = self.leftFollower.calculate(self.l_encoder.get())
            r = self.rightFollower.calculate(self.r_encoder.get())

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
            self.robot_drive.tankDrive(-l, -r)

        # self.addSequential(MoveTimed(1), 2.0)
        # self.addSequential(SpinTimed(0.25), 2.0)
        # self.addSequential(MoveTimed(1), 2.0)
        # self.addSequential(SpinTimed(0.25), 2.0)
        # self.addSequential(MoveTimed(1), 2.0)
        # self.addSequential(SpinTimed(0.25), 2.0)
        # self.addSequential(MoveTimed(1), 2.0)
        # self.addSequential(SpinTimed(2), 2.0)
        # this is just filler code we can change this later
