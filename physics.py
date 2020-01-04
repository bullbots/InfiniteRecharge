import pprint

from pyfrc.physics import drivetrains
from pyfrc.sim import get_user_renderer


class PhysicsEngine:

    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.drivetrain = drivetrains.TwoMotorDrivetrain()
        self.initial = True
        self.count = 0

    def update_sim(self, hal_data, now, tm_diff):
        # print(hal_data)
        # user_renderer = get_user_renderer()
        # user_renderer.clear()
        #
        # if self.count % 3 == 0:
        #     user_renderer.draw_line([(0, 0), (5, 5)], color='#0000ff', robot_coordinates=True, arrow=False)
        # elif self.count % 3 == 1:
        #     user_renderer.draw_line([(0, 0), (5, 5)], color='#00ff00', robot_coordinates=True, arrow=False)
        # elif self.count % 3 == 2:
        #     user_renderer.draw_line([(0, 0), (5, 5)], color='#ff0000', robot_coordinates=True, arrow=False)
        #     self.count = -1

        self.count += 1

        if self.initial:
            self.initial = False
            # pprint.pprint(hal_data["CAN"])
            # for key in hal_data["sparkmax-5"].keys():
            #     print(key)
        # Simulate the drivetrain
        left_master_motor = -hal_data["CAN"][1]["value"]
        right_master_motor = hal_data["CAN"][3]["value"]

        speed, rotation = self.drivetrain.get_vector(left_master_motor, right_master_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)
