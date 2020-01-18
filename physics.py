import pprint

from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

import math

class PhysicsEngine:

    def __init__(self, physics_controller):
        self.physics_controller = physics_controller

        bumper_width = 3.25 * units.inch

        self.drivetrain = tankmodel.TankModel.theory(
            motor_config=motor_cfgs.MOTOR_CFG_CIM,
            robot_mass=110 * units.lb,
            gearing=10.71,
            nmotors=2,
            x_wheelbase=22 * units.inch,
            robot_width=23 * units.inch + bumper_width * 2,
            robot_length=32 * units.inch + bumper_width * 2,
            wheel_diameter=6 * units.inch
        )

        # Precompute the encoder constant
        # -> encoder counts per revolution / wheel circumfrence
        self.kEncoder = 360 / (0.5 * math.pi)

        self.l_distance = 0
        self.r_distance = 0
        self.first = True

    def update_sim(self, hal_data, now, tm_diff):
        left_master_motor = -hal_data["CAN"][1]["value"]
        right_master_motor = hal_data["CAN"][3]["value"]

        can_motor = hal_data["CAN"][1]["quad_position"]
        print(f"left: {left_master_motor}, can_motorL {can_motor}")

        if self.first:
            self.first = False
            pprint.pprint(hal_data["CAN"][1]["quad_position"])

        x, y, angle = self.drivetrain.get_distance(
            left_master_motor,
            right_master_motor,
            tm_diff
        )
        self.physics_controller.distance_drive(x, y, angle)

        # Update encoders
        self.l_distance += self.drivetrain.l_velocity * tm_diff
        self.r_distance += self.drivetrain.r_velocity * tm_diff

        hal_data["encoder"][0]["count"] = int(self.l_distance * self.kEncoder)
        hal_data["encoder"][1]["count"] = int(self.r_distance * self.kEncoder)
