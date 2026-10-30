import random

import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        # Asteroid.containers (set in main.py) adds it to the asteroids, updatable and drawable groups
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the asteroid as a circle outline (a width > 0 means it isn't filled)
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        # Move in a straight line at constant velocity, scaled by elapsed time
        self.position += self.velocity * dt

    def split(self) -> None:
        """Destroy this asteroid, spawning two smaller ones if it's big enough."""
        # Always remove this asteroid. Its attributes can still be read
        # below, because kill() only removes it from its groups.
        self.kill()

        # Smallest size: it just disappears
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        # Send the two pieces off at a random angle either side of the original direction
        angle = random.uniform(20, 50)
        velocity_a = self.velocity.rotate(angle)
        velocity_b = self.velocity.rotate(
            -angle
        )  # rotate() returns a new vector; the original is unchanged

        # Each split drops one size level (large → medium → small)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Spawn both pieces where the original was; they speed up a little (1.2x) when they split
        asteroid_a = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_a.velocity = velocity_a * 1.2

        asteroid_b = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_b.velocity = velocity_b * 1.2
