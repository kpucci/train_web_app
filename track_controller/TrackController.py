"""
VITAL

Attributes:
Inputs:     authority, speed, occupancy, switch state, light state, crossing state
Functions:  control switching of track, control railway crossing, detect broken
            rails, detect presence of trains, send state of track to ctc, send
            state of railway crossing to ctc, send state of signsl to ctc, send
            occupancy to ctc
"""

class TrackController:

    def __init__(self):
        """Initialize a track controller."""
