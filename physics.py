from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


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

    def update_sim(self, hal_data, now, tm_diff):
        left_master_motor = -hal_data["CAN"][1]["value"]
        right_master_motor = hal_data["CAN"][3]["value"]

        x, y, angle = self.drivetrain.get_distance(left_master_motor, right_master_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
