import numpy
import sys

# try to import the GPIO module on the raspberry pi
# fallback to the mock implementation for dev and testing
try:
    import RPi.GPIO as gpio
except ImportError:
    import components.gpio as gpio


def get_random_colors(quantity=1, seed=1):
    """Generates an array of a random color value.

    Keyword arguments:
    quantity -- How many colors inside the array (default: 1)
    """
    numpy.random.seed(seed)
    return numpy.random.randint(0, 255, size=(quantity, 3),
                                dtype="uint8")


def get_next_breakpoint(distanceToGround, breakpoints):
    """Returns the next breakpoint based on the current distance
    from the ground.

    Keyword arguments:
    quantity -- How many colors inside the array (default: 1)
    """
    for breakpoint in breakpoints.values():
        if distanceToGround < breakpoint:
            return breakpoint


def create_debug_logger(shouldLog):
    """
    Factory function to create a debug logger that only
    prints a message to console if passed argument is truthy.

    arguments:
    shouldLog -- If the messsage should be printed to console or not
    """
    shouldLog = shouldLog

    def log(message):
        if shouldLog:
            print(message)
    return log


def omit_range(new, old, range):
    return new if abs(new - old) <= range else old

def save_shutdown(message='Script exited.', cleanup=None):
    """
    Exits the scripts cleanly and executes a passed cleanup
    function beforehand. Also prints an exit message and does a
    gpio cleanup.

    Keyword arguments:
    message  -- The exit message
    cleanup -- The cleanup function that is executed before the exit
    """
    # Call cleanup function is exists
    if not None and callable(cleanup):
        cleanup()

    # cleanup gpio pins and print shutdown message
    gpio.cleanup()
    print(message)

    # exit cleanly
    sys.exit(0)

