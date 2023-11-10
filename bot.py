# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    MapProxy,
    Vector,
    WeatherForecast,
    config,
)
from vendeeglobe.utils import distance_on_surface

CREATOR = "Argos"  # This is your team name


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition
    for the Argos
    """

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.avatar = 1  # Optional attribute
        self.course = [
            # Checkpoint(latitude=43.797109, longitude=-11.264905, radius=50),

            # 0
            Checkpoint(latitude=18.579, longitude=-67.780, radius=10),
            # 1
            Checkpoint(latitude=17.775, longitude=-68.250, radius=10),
            # 2
            Checkpoint(latitude=9.813, longitude=-79.850, radius=5),
            # 3
            Checkpoint(latitude=6.824, longitude=-79.597, radius=5),

            # 4
            Checkpoint(latitude=2.806318, longitude=-168.943864, radius=1990.0),
            # 5
            Checkpoint(latitude=2.970, longitude=127.167, radius=10.0),
            # 6
            Checkpoint(latitude=2.970, longitude=125.167, radius=10.0),
            # 7
            Checkpoint(latitude=2.350, longitude=119.839, radius=10.0),
            # 8
            Checkpoint(latitude=-8, longitude=115.70, radius=10.0),
            # 9
            Checkpoint(latitude=-8.994, longitude=115.70, radius=10.0),

            # 10
            Checkpoint(latitude=-15.668984, longitude=77.674694, radius=1190.0),
            # 11
            Checkpoint(latitude=14.562, longitude=54.053, radius=10.0),
            # 12
            Checkpoint(latitude=12.104, longitude=43.783, radius=10.0),
            # 13
            Checkpoint(latitude=19.699, longitude=38.441, radius=10.0),
            # 14
            Checkpoint(latitude=27.176, longitude=34.209, radius=10.0),

            # 15
            Checkpoint(latitude=29.3894, longitude=32.6486, radius=10.0),
            # 16
            Checkpoint(latitude=31.3894, longitude=32.41, radius=10.0),

            # 17
            Checkpoint(latitude=31.8, longitude=32.410, radius=10.0),


            Checkpoint(latitude=35.8, longitude=15.410, radius=10.0),

            # 17
            Checkpoint(latitude=38.857, longitude=4.555, radius=300.0),
            # 18
            Checkpoint(latitude=35.960, longitude=-3.680, radius=10.0),
            # 19
            Checkpoint(latitude=36.00, longitude=-6.757, radius=10.0),

            # 20
            Checkpoint(latitude=36.950, longitude=-9.327, radius=10.0),

            # west of portugal
            Checkpoint(latitude=39.150, longitude=-9.7, radius=10.0),

            # North west portugal
            Checkpoint(latitude=43.213, longitude=-9.514, radius=10.0),

            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: WeatherForecast,
        world_map: MapProxy,
    ):
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            The weather forecast for the next 5 days.
        world_map:
            The map of the world: 1 for sea, 0 for land.
        """
        instructions = Instructions()
        for ch in self.course:
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            jump = dt * np.linalg.norm(speed)
            if dist < 2.0 * ch.radius + jump:
                instructions.sail = min(ch.radius / jump, 1)
            else:
                instructions.sail = 1.0
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break

        return instructions
