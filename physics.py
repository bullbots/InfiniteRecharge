import pprint

from pyfrc.physics import drivetrains
from pyfrc.sim import get_user_renderer


class PhysicsEngine:

    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.drivetrain = drivetrains.TwoMotorDrivetrain()
        self.second_drivetrain = drivetrains.Two
        self.initial = True
        self.count = 0

    def update_sim(self, hal_data, now, tm_diff):

        self.count += 1

        if self.initial:
            self.initial = False

        # Simulate the drivetrain
        left_master_motor = -hal_data["CAN"][1]["value"]
        right_master_motor = hal_data["CAN"][3]["value"]

        speed, rotation = self.drivetrain.get_vector(left_master_motor, right_master_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)
