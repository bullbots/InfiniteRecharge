from wpilib.command import CommandGroup, WaitCommand

from commands.move_timed import MoveTimed
from commands.spin_timed import SpinTimed

class AutonomusDriving(CommandGroup):

    def __init__(self):
        super().__init__()
        self.addSequential(MoveTimed(1), 2.0)
        self.addSequential(SpinTimed(0.25), 2.0)
        self.addSequential(MoveTimed(1), 2.0)
        self.addSequential(SpinTimed(0.25), 2.0)
        self.addSequential(MoveTimed(1), 2.0)
        self.addSequential(SpinTimed(0.25), 2.0)
        self.addSequential(MoveTimed(1), 2.0)
        self.addSequential(SpinTimed(2), 2.0)
        # this is just filler code we can change this later
