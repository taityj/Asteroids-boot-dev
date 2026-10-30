import pygame
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Facing direction in degrees (0 = pointing along +y)
        self.shot_cooldown = 0  # Seconds until the player can shoot again

    def triangle(self) -> list[pygame.Vector2]:
        """Return the three corner points of the ship, based on position and rotation."""
        # Unit vector pointing the way the ship faces
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Vector at 90° to forward, scaled to set how wide the ship's base is
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius  # Nose
        b = self.position - forward * self.radius - right  # Back-left corner
        c = self.position - forward * self.radius + right  # Back-right corner
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the ship as a triangle outline
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        # A negative dt turns the ship the other way
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        # Count down the shot cooldown (it can go below 0; shoot() only checks > 0)
        self.shot_cooldown -= dt

        keys = pygame.key.get_pressed()

        # A/D turn; W/S move forward/backward (negative dt reverses direction)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        # Start with a unit vector pointing "forward" before any rotation
        unit_vector = pygame.Vector2(0, 1)
        # Turn it to match the direction the ship is facing
        rotated_vector = unit_vector.rotate(self.rotation)
        # Scale by speed and elapsed time so movement is frame-rate independent
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        # Still cooling down from the last shot, so do nothing
        if self.shot_cooldown > 0:
            return
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Spawn a shot at the ship's centre (Shot.containers adds it to the groups)
        shot = Shot(self.position.x, self.position.y)
        # Fire it in the direction the ship is facing, at shooting speed
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
