import random
from collections.abc import Callable

import pygame
from asteroid import Asteroid
from constants import *

# An edge is a pair: (direction asteroids move in, function that picks a spawn point on that edge)
Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    """Invisible spawner that periodically creates asteroids just off-screen."""

    containers: pygame.sprite.Group

    # One entry per screen edge. Each lambda takes a number from 0 to 1 and returns
    # a point along that edge, pushed out by ASTEROID_MAX_RADIUS so that even the
    # largest asteroid starts fully off-screen and drifts in.
    edges: list[Edge] = [
        # Left edge: move right
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        # Right edge: move left
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        # Top edge: move down (pygame's y-axis points downwards)
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        # Bottom edge: move up
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        # Not a CircleShape, so it joins its groups directly (only `updatable`, set in main.py)
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0  # Seconds since the last asteroid was spawned

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        # Asteroid.containers adds the new asteroid to its groups automatically
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        # Spawn one asteroid every ASTEROID_SPAWN_RATE_SECONDS
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # Spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            # Angle it up to 30° off straight-in so asteroids don't all travel in parallel
            velocity = velocity.rotate(random.randint(-30, 30))
            # Pick a random point along the chosen edge
            position = edge[1](random.uniform(0, 1))
            # Choose a size: kind 1 = small, 2 = medium, 3 = large
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
