import pygame
import math

def draw_circles_with_converging_rings(screen, circles):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Font for the numbers

    # Dictionary to track when the ring converges with each circle
    convergence_times = {}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Check if the click is within any of the circles
                for circle in circles:
                    dx = pos[0] - circle['pos'][0]
                    dy = pos[1] - circle['pos'][1]
                    distance = math.sqrt(dx * dx + dy * dy)
                    if distance < circle['radius']:
                        circle['draw_circle'] = False
                        circle['ring_radius'] = 0  # Also hide the ring

        screen.fill((0, 0, 0))  # Fill the screen with black

        for i, circle in enumerate(circles):
            # Delay before drawing the circle and its ring
            if pygame.time.get_ticks() < circle['start_time']:
                continue

            # Draw the main circle if the flag is set
            if circle['draw_circle']:
                pygame.draw.circle(screen, circle['color'], circle['pos'], circle['radius'])
                text = font.render(str(i + 1), True, (0, 0, 0))  # Render the number
                text_rect = text.get_rect(center=circle['pos'])  # Center the text
                screen.blit(text, text_rect)  # Draw the text

            # Draw the converging ring
            if circle['ring_radius'] > circle['radius']:
                pygame.draw.circle(screen, circle['color'], circle['pos'], circle['ring_radius'], 1)
                circle['ring_radius'] -= circle['speed']
            elif circle['draw_circle'] is not None:  # Only track the convergence time once
                # Set the convergence time
                convergence_times[i] = pygame.time.get_ticks() + 500  # Hardcoded to 500 milliseconds
                circle['draw_circle'] = None  # Prevent this branch from being executed again

            # Hide the circle after the convergence time ends
            if i in convergence_times and pygame.time.get_ticks() >= convergence_times[i]:
                circle['draw_circle'] = False
                del convergence_times[i]

        pygame.display.flip()
        clock.tick(60)

screen = pygame.display.set_mode((800, 600))

# Define your circles here
circles = [
    {'color': (255, 255, 255), 'pos': (400, 300), 'radius': 40, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 0},
    {'color': (255, 255, 255), 'pos': (100, 100), 'radius': 40, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 1000},
    {'color': (255, 255, 255), 'pos': (700, 100), 'radius': 40, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 2000},
    {'color': (255, 255, 255), 'pos': (100, 500), 'radius': 40, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 3000},
    {'color': (255, 255, 255), 'pos': (700, 500), 'radius': 40, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 4000}
]

draw_circles_with_converging_rings(screen, circles)
