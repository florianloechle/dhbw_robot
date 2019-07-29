# try to import the GPIO module on the raspberry pi
# fallback to the mock implementation for dev and testing
try:
    import RPi.GPIO as gpio
except ImportError:
    import components.gpio as gpio


class Engine:
    """
    Base class for all engines.
    Provides basic functionality like forwards, backwards and stop.
    """

    # Possible engine states
    state = {
        "FORWARD": (gpio.HIGH, gpio.LOW, gpio.HIGH),
        "BACKWARD": (gpio.LOW, gpio.HIGH, gpio.HIGH),
        "STOP": (gpio.LOW, gpio.LOW, gpio.LOW),
    }

    def __init__(self, pinConfiguration):
        """
        Initalizes a new engine object with the given pin configuration.
        The configuration should include two output and one pwm pin.

        Keyword arguments:
        pinConfiguraton (tuple) -- The pins on the pi board (pin1,pin2,pinpwm)
        """
        pin1, pin2, pinPWM = pinConfiguration

        # Pins
        self.pin1 = pin1
        self.pin2 = pin2
        self.pinPWM = pinPWM

        # Current powerlevel
        self.power = 0

        # setup pins as outputs
        gpio.setup((self.pin1, self.pin2, self.pinPWM),
                   gpio.OUT)

        # initialize pwm with 100%
        self.pwm = gpio.PWM(self.pinPWM, 100)

    def set_state(self, state, power):
        """
        Sets output pins to the given state.

        Keyword arguments:
        state -- The engine state to set
        power -- The pwm powerlevel to set
        """
        self.power = power
        if power != 0:
            self.pwm.start(self.power)

        gpio.output((self.pin1, self.pin2, self.pinPWM), state)

    def forward(self, power):
        """
        Engine going forwards with the given pwm power.
        """
        self.set_state(Engine.state.get('FORWARD'), power)

    def backward(self, power):
        """
        Engine going backwards with the given pwm power.
        """
        self.set_state(Engine.state.get('BACKWARD'), power)

    def stop(self):
        """
        Stops the engine and sets power to zero.
        """
        self.set_state(Engine.state.get('STOP'), 0)


class Claw(Engine):
    def open_with(self, power):
        self.forward(power)

    def close_with(self, power):
        self.backward(power)


class Drive(Engine):
    def forward_with(self, power):
        self.forward(power)

    def backward_with(self, power):
        self.backward(power)


class Lift(Engine):
    def upward_with(self, power):
        self.forward(power)

    def downward_with(self, power):
        self.backward(power)
