import sys

import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Set up pygame, the window, and a clock to control the frame rate
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0.0  # Seconds since the last frame; used to make movement frame-rate independent

    # Groups let us update, draw, and check collisions for many objects at once
    asteroids = pygame.sprite.Group()  # Every asteroid, for collision checks
    updatable = pygame.sprite.Group()  # Everything that needs update(dt) each frame
    drawable = pygame.sprite.Group()  # Everything that needs draw(screen) each frame
    shots = pygame.sprite.Group()  # Every bullet, for collision checks

    # Any object created from these classes is automatically added to these groups
    # (CircleShape.__init__ reads the class's `containers` attribute)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)  # Spawns asteroids; isn't drawn itself
    Shot.containers = (shots, updatable, drawable)

    # Create the player in the centre of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Not referenced again: creating it adds it to `updatable`, where it spawns asteroids
    asteroid_field = AsteroidField()

    # Main game loop: runs once per frame
    while True:
        log_state()  # Record the game state for boot.dev's tests

        # Exit cleanly when the window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Move everything: player input, asteroids, shots, and asteroid spawning
        updatable.update(dt)

        # Check collisions using the positions from this frame
        for asteroid in asteroids:
            # An asteroid touching the player ends the game
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            # A shot hitting an asteroid destroys the shot and splits the asteroid
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    break  # This asteroid is gone; stop checking it against other shots

        # Clear the screen, then draw every visible object
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        # Show the finished frame
        pygame.display.flip()

        # Limit to 60 FPS and convert the elapsed milliseconds to seconds
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
