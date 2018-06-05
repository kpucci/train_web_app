"""
Attributes: length, height, width, mass, crew count, passenger count
Inputs:     authority (wayside), setpoint speed command, brake command, speed limit,
            acceleration limit, deceleration limit, route information system, temperature
            control, door open, door close, transponder input, track circuit input,
            light controller for tunnels, emergency brake from passenger
Failure modes:  train engine failure, signal pickup failure, brake failure
"""

class Train:
    crewCount = 0
    passCount = 0
    carLength = 0.0
    carHeight = 0.0
    carMass = 0.0

    def __init__(self, name="", numCars=0):
        """Initialize a train object."""
        self.name = name
        self.mass = carMass * numCars
        self.length = carLength * numCars
        self.height = carHeight
        self.width = carWidth

    def accelerate(self):
        """Accelerate the train."""

    def decelerate(self):
        """Decelerate the train."""

    def brake(self):
        """Apply the brakes."""

    def emergencyBrake(self):
        """Apply the emergency brake."""

    def openDoor(self):
        """Open the door."""

    def closeDoor(self):
        """Close the door."""

    def turnLightOn(self):
        """Turn light on."""

    def turnLightOff(self):
        """Turn light off."""
