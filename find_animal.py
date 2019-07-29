import click
import time
import sys
import os

# import robot components
from components.engine import Drive, Claw, Lift
from components.sensor import Sensor
from components.detector import NeuralNetworkDetector
from components.camera import Camera

# import necessary function from utils
from shared.utils import create_debug_logger, save_shutdown, get_next_breakpoint

# try to import the GPIO module on the raspberry pi
# fallback to the mock implementation for dev and testing
try:
    import RPi.GPIO as gpio
except ImportError:
    print('Failed to import GPIO module, using mock instead.')
    import components.gpio as gpio


@click.command()
@click.argument('animal',
                type=click.Choice(['frog', 'turtle', 'dino', 'leopard', 'tomato']), required=True)
@click.option('--debug/--no-debug', default=False)
def main(animal, debug):
    """
    A robot to grab specific animals out of a shelf. The robot will
    grab the animal you provide if it is supported. You can optionally enable
    debug mode which enables logging throughout the whole process.
    """

    try:
        find_animal(animal, debug)
        print('Successfully fetched ' + str(animal).upper() + '.')
    except KeyboardInterrupt:
        pass

    gpio.cleanup()
    sys.exit(0)


class Options:

    # Init options with configuration values
    def __init__(self):

        # Pin configuration fpr all engines
        self.claw_pins = (35, 37, 40)
        self.lift_pins = (31, 33, 38)
        self.drive_pins = (32, 29, 36)

        # Pin configuratin for all sensors
        self.heightsensor_pins = (16, 22)
        self.distancesensor_pins = (12, 7)

        # Power configuration for all engines
        self.claw_power = 50
        self.lift_power = 100
        self.drive_power = 35

        # Breakpoint configuration in cm
        self.shelf_breakpoints = {
            1: 5,
            2: 29,
            3: 51,
            4: 76
        }

        # Distance configuration
        self.shelf_distance = 9
        self.destination_distance = 63
        self.ground_distance = 11


def find_animal(animal, debug=False):

    # Setup raspberry pi board and options
    gpio.setmode(gpio.BOARD)
    opts = Options()
    log = create_debug_logger(debug)

    # Start the sequence
    log('Started finding ' + str(animal).upper() + '.')

    log('Phase: Going upwards.')
    # Init heightsensor and liftengine
    height_sensor = Sensor(opts.heightsensor_pins)
    lift_engine = Lift(opts.lift_pins)
    camera = Camera(0)
    detector = NeuralNetworkDetector(camera, debug)

    isLowerShelf = False
    startTime = time.time()
    while time.time() < startTime + 3:
        isLowerShelf = detector.detect(animal)

    if not isLowerShelf:

        found = False
        while not found:
            found = detector.detect(animal)
            lift_engine.upward_with(opts.lift_power)
            if height_sensor.get_distance() > 60:
                found = True

        current_distance = height_sensor.get_distance()
        target_breakpoint = get_next_breakpoint(
            current_distance, opts.shelf_breakpoints)

        while height_sensor.get_distance() < target_breakpoint:
            lift_engine.upward_with(opts.lift_power)
            time.sleep(0.05)

    log('Phase: Driving forwards into shelf.')
    # Init distancesensor and driveengine
    distance_sensor = Sensor(opts.distancesensor_pins)
    drive_engine = Drive(opts.drive_pins)

    while distance_sensor.get_distance() > opts.shelf_distance:
        drive_engine.forward_with(opts.drive_power)
        lift_engine.upward_with(20)
        time.sleep(0.05)

    drive_engine.stop()
    log('Phase: Closing claw with ' +
        str(animal).upper() + '.')

    # Init clawengine
    claw_engine = Claw(opts.claw_pins)

    claw_engine.open_with(opts.claw_power)
    time.sleep(1.2)

    log('Phase: Driving backwards to destination')
    while distance_sensor.get_distance() < opts.destination_distance:
        drive_engine.backward(opts.drive_power)
        time.sleep(0.1)

    log('Phase: Arrived at destinatiion.')
    drive_engine.stop()

    if not isLowerShelf:
        log('Phase: Going downwards to ' +
            str(opts.ground_distance) + 'cm.')
        while height_sensor.get_distance() > opts.ground_distance:
            lift_engine.downward_with(opts.lift_power)
            time.sleep(0.05)

        lift_engine.stop()

    time.sleep(1)
    log('Phase: Opening claw in destination.')
    claw_engine.close_with(opts.claw_power)
    time.sleep(1.2)


if __name__ == '__main__':
    main()
