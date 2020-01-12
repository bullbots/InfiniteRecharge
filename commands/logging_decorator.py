import logging

from wpilib.command.command import Command


def logging_command(cls):
    class LoggingWrapper(Command):
        def __init__(self, *args):
            super().__init__(name=cls.__name__)
            self.logger = logging.getLogger(name=cls.__name__)
            self.wrapped = cls(*args)
            requirements = self.wrapped.getRequirements()
            for requirement in requirements:
                self.requires(requirement)

        def _initialize(self):
            self.wrapped._initialize()

        def initialize(self):
            self.logger.info("initialize")
            self.wrapped.initialize()

        def execute(self):
            # self.logger.info("execute")
            self.wrapped.execute()

        def _execute(self):
            self.wrapped._execute()

        def isFinished(self):
            return self.wrapped.isFinished()
            # if finished:
            #     self.logger.info("finished")
            # return finished

        def end(self):
            self.logger.info("end")
            self.wrapped.end()

        def interrupted(self):
            self.logger.info("interrupted")
            self.wrapped.interrupted()

    return LoggingWrapper