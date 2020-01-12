from wpilib.command import Command
from wpilib.smartdashboard import SmartDashboard
from commands.logging_decorator import logging_command

@logging_command
class JoystickDrive(Command):
    """Get input from joysticks and feed it into diffdrive method of the drivetrain"""

    def __init__(self):
        super().__init__(subsystem=Command.getRobot().drivetrain)

    def execute(self):
        joyX = Command.getRobot().oi.stick.getX()
        joyY = Command.getRobot().oi.stick.getY()

        SmartDashboard.putNumber("Joystick X", joyX)
        SmartDashboard.putNumber("Joystick y", joyY)

        Command.getRobot().drivetrain.diffdrive(joyX, -joyY)

    def isFinished(self):
        return False
