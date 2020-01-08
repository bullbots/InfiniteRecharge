from wpilib.command import Command


class JoystickDrive(Command):
    """Get input from joysticks and feed it into diffdrive method of the drivetrain"""

    def __init__(self):
        super().__init__(subsystem=Command.getRobot().drivetrain)

    def execute(self):
        joyX = Command.getRobot().oi.stick.getX()
        joyY = Command.getRobot().oi.stick.getY()

        Command.getRobot().drivetrain.diffdrive(joyX, -joyY)

    def isFinished(self):
        return False
