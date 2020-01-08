import math


# TODO: Create Decorator to automatically run drivetrain outputs through CheesyDriveHelper?

class DriveHelper():
    """A helper class to take joystick input and map it to trajectory instead of motor output"""

    # Static Variables
    throttle_deadband = 0.02
    wheel_deadband = 0.02
    high_wheel_nonlinearity = 0.65
    low_wheel_nonlinearity = 0.5
    high_neg_inertia_scalar = 4.0
    low_neg_inertia_threshold = 0.65
    low_neg_inertia_turn_scalar = 3.5
    low_neg_inertia_close_scalar = 4.0
    low_neg_inertia_far_scalar = 5.0
    high_sensitivity = 0.65
    low_sensitivity = 0.65
    quick_stop_deadband = 0.5
    quick_stop_weight = 0.1
    quick_stop_scalar = 5.0

    def __init__(self):
        self.old_wheel = 0.0
        self.quick_stop_accumulator = 0.0
        self.neg_inertia_accumulator = 0.0

    def DriveSignal(self, throttle: float, wheel: float, quick_turn: bool, high_gear: bool):
        """Converts joystick to motor outputs"""

        wheel = DriveHelper._handle_deadband(wheel, DriveHelper.wheel_deadband)
        throttle = DriveHelper._handle_deadband(throttle, DriveHelper.throttle_deadband)

        neg_inertia = wheel - self.old_wheel
        self.old_wheel = wheel

        wheel_nonlinearity = 0
        if high_gear:
            wheel_nonlinearity = DriveHelper.high_wheel_nonlinearity
            denominator = math.sin(math.pi / 2 * wheel_nonlinearity)

            wheel = math.sin(math.pi / 2 * wheel_nonlinearity * wheel) / denominator
            wheel = math.sin(math.pi / 2 * wheel_nonlinearity * wheel) / denominator
        else:
            wheel_nonlinearity = DriveHelper.low_wheel_nonlinearity
            denominator = math.sin(math.pi / 2 * wheel_nonlinearity)

            wheel = math.sin(math.pi / 2 * wheel_nonlinearity * wheel) / denominator
            wheel = math.sin(math.pi / 2 * wheel_nonlinearity * wheel) / denominator
            wheel = math.sin(math.pi / 2 * wheel_nonlinearity * wheel) / denominator

        left_pwm, right_pwm, over_power = 0, 0, 0
        sensitivity = 0
        angular_power, linear_power = 0, 0

        neg_inertiaScalar = 0
        if high_gear:
            neg_inertiaScalar = DriveHelper.high_neg_inertia_scalar
            sensitivity = DriveHelper.high_sensitivity
        else:
            if wheel * neg_inertia > 0:
                neg_inertiaScalar = DriveHelper.low_neg_inertia_turn_scalar
            else:
                if abs(wheel) > DriveHelper.low_neg_inertia_threshold:
                    neg_inertiaScalar = DriveHelper.low_neg_inertia_far_scalar
                else:
                    neg_inertiaScalar = DriveHelper.low_neg_inertia_close_scalar
            sensitivity = DriveHelper.low_sensitivity

        neg_inertiaPower = neg_inertia * neg_inertiaScalar
        self.neg_inertia_accumulator += neg_inertiaPower

        wheel = wheel + self.neg_inertia_accumulator
        if self.neg_inertia_accumulator > 1:
            self.neg_inertia_accumulator -= 1
        elif self.neg_inertia_accumulator < -1:
            self.neg_inertia_accumulator += 1
        else:
            self.neg_inertia_accumulator = 0

        linear_power = throttle

        if quick_turn:
            if abs(linear_power) < DriveHelper.quick_stop_deadband:
                alpha = DriveHelper.quick_stop_weight
                self.quick_stop_accumulator = (1 - alpha) * self.quick_stop_accumulator + alpha * DriveHelper._limit(wheel,
                                                                                                         1) * self.quick_stop_scalar

            over_power = 1
            angular_power = wheel
        else:
            over_power = 0
            angular_power = abs(throttle) * wheel * sensitivity - self.quick_stop_accumulator

            if self.quick_stop_accumulator > 1:
                self.quick_stop_accumulator -= 1
            elif self.quick_stop_accumulator < -1:
                self.quick_stop_accumulator += 1
            else:
                self.quick_stop_accumulator = 0

        right_pwm = left_pwm = linear_power
        left_pwm += angular_power
        right_pwm -= angular_power

        if left_pwm > 1:
            right_pwm -= over_power * (left_pwm - 1)
            left_pwm = 1
        elif right_pwm > 1:
            left_pwm -= over_power * (right_pwm - 1)
            right_pwm = 1
        elif left_pwm < -1:
            right_pwm += over_power * (-1 - left_pwm)
            left_pwm = -1
        elif right_pwm < -1:
            left_pwm += over_power * (-1 - right_pwm)
            right_pwm = -1

        return (left_pwm, right_pwm)

    @staticmethod
    def _handle_deadband(val: float, deadband: float):
        """Applies deadband to a value"""
        return abs(val) > abs(deadband) if val else 0

    @staticmethod
    def _limit(val: float, max: float):
        """Constrains a Value between max and -max"""
        return abs(val) > abs(max) if math.copysign(max, val) else val
