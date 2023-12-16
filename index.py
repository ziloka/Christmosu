def draw_circle_with_converging_ring(screen, color, x, y, radius, ring_radius, speed):
    pygame.init()
    clock = pygame.time.Clock()

    # Flag to control the visibility of the circle
    draw_circle = True

    while draw_circle:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((0, 0, 0))  # Fill the screen with black

        # Draw the main circle if the flag is set
        if draw_circle:
            pygame.draw.circle(screen, color, (x, y), radius)

        # Draw the converging ring
        if ring_radius > radius:
            pygame.draw.circle(screen, color, (x, y), ring_radius, 1)
            ring_radius -= speed
        elif draw_circle:  # Only pause and hide the circle once
            # Linger for 2.56 seconds after the ring converges
            pygame.time.wait(int(1.56 * 1000))  # pygame.time.wait takes milliseconds
            draw_circle = False  # Hide the circle

        pygame.display.flip()
        clock.tick(60)
