# InfiniteRecharge

## Contributing

Here are the processes for contributing any code to the repo

1. Fetch and pull the develop branch
2. Open a new branch named feature/[your feature name here]. For instance, if we are adding pid to the drivetrain, we would open the branch feature/drivetrain_pid
3. Publish the branch to Github using Github Desktop
4. Make your changes
5. Test your code using `python robot.py sim` and `python robot.py test`
6. Commit your changes with a short message about what you did
7. Push the branch to github, again using Github Desktop
8. Go onto github in a browser and submit a pull request

## Robot Structure

Here I am going to attempt to give you a reference for how our robot code is structured and where you can find things

### robot.py
This is the main hub of our code where everything is pulled in. It is responsible for scheduling commands and handling subsystems, though we write very little of that code. It is also useful for logging.

#### `robotInit(self)`
This method runs when we start our robot at the very beginning. You should initialize all subsystems here. An important function is created here with the line `Command.getRobot = lambda: self`. Though the syntax is a little complicated, all you need to know is we are adding a function to `Command` which will give you the robot. We will use this in commands and subsystems to interact with our robot.

#### `robotPeriodic(self)`
This method runs every 20ms as long as the robot is on. It is useful for logging.

#### Init vs Periodic
There are 6 more methods we can override in robot.py, all following a similar naming schema. The prefixes are autonomous, teleop, and disabled, all of which are followed by Init or Periodic. They will run at the start of a mode if it ends with Init, and every 20ms during a mode if it ends with Periodic. These all have various uses.

### subsystems/
This folder is where all of our subsystems are declared. Here we initialize and configure all hardware and create methods for interacting with that hardware. Remember, structure your subsystems so all related hardware are part of one subsystem, since only one command can run on a subsystem at a time (and subsystems don't communicate with each other).

#### `__init__(self)`
This is where we initalize all hardware such as motor controllers and solenoids. Configuration of the hardware should also occur here.

#### `initDefaultCommand(self)`
This is where we specify the default command to be run if no other command is being run. For instance, if we have an elevator we will want to have a default command that will hold the elevator at a specific location. This is used in the drivetrain subsystem to set the default command to joystick drive.

### robot_map.py
This is where we define all our ports for our various hardware. If you are adding or editing in this file just mimic the naming schema that is already present. You will pull port numbers from this file into subsystems when you initialize hardware.

### commands/
This is where we define all the commands that we can run during a match. This does the doing of our robot. Look at the syntax for the init method in already existing commands because it is a little funky.

#### `initalize(self)`
This runs once when the command is started. All PID operations should be done here, otherwise they should start in execute. This is useful for command specific configuration

#### `execute(self)`
This is the command that does the doing, running every 20ms until the command finishes

#### `isFinished(self)`
This should return a boolean that tells the command whether it has finished. If your command is moving a motor to a position, then this should test whether you are at that position. If you want your command to never end, return false

### oi.py
This is where we configure all input for our robot. For instance, we create all buttons and joysticks here. We also map commands to inputs here, so if you want a button to start a command, do it here.

### constants.py
This is just a file containing various constants we use throughout the robot. If your code relies on a number that is not inherently obvious, put it here.
