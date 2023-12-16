import pygame

# Define a custom event for the end of the linger time
END_LINGER_EVENT = pygame.USEREVENT + 1

def draw_circles_with_converging_rings(screen, circles):
    pygame.init()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == END_LINGER_EVENT:
                # When the linger time ends, hide the circle
                circles[event.circle_index]['draw_circle'] = False

        screen.fill((0, 0, 0))  # Fill the screen with black

        for i, circle in enumerate(circles):
            # Delay before drawing the circle and its ring
            if pygame.time.get_ticks() < circle['start_time']:
                continue

            # Draw the main circle if the flag is set
            if circle['draw_circle']:
                pygame.draw.circle(screen, circle['color'], circle['pos'], circle['radius'])

            # Draw the converging ring
            if circle['ring_radius'] > circle['radius']:
                pygame.draw.circle(screen, circle['color'], circle['pos'], circle['ring_radius'], 1)
                circle['ring_radius'] -= circle['speed']
            elif circle['draw_circle']:  # Only pause and hide the circle once
                # Schedule the end of the linger time
                pygame.time.set_timer(END_LINGER_EVENT, int(circle['linger_time'] * 1000), True)
                pygame.event.post(pygame.event.Event(END_LINGER_EVENT, circle_index=i))
                circle['draw_circle'] = None  # Prevent this branch from being executed again

        pygame.display.flip()
        clock.tick(60)

screen = pygame.display.set_mode((800, 600))

# Define your circles here
circles = [
    {'color': (255, 255, 255), 'pos': (400, 300), 'radius': 50, 'ring_radius': 100, 'speed': 1, 'linger_time': 2.56, 'draw_circle': True, 'start_time': 0},
    {'color': (255, 0, 0), 'pos': (100, 100), 'radius': 50, 'ring_radius': 100, 'speed': 1, 'linger_time': 3.56, 'draw_circle': True, 'start_time': 1000}
]

draw_circles_with_converging_rings(screen, circles)
