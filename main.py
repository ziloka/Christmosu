import pygame
import math
import random
import winsound
import time
def draw_circles_with_converging_rings(screen, circles):
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)  # Font for the numbers
    hit_sound = pygame.mixer.Sound('soft-hitsoft.wav')
    # Initialize the score
    score = 0
    combo=1
    max_combo=0
    hits=0
    miss=0
    finished=True
    while finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # if combo > max_combo:
                #     max_combo = combo
                # return [score, max_combo, hits, miss]  # Return the score when the game ends
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Check if the click is within any of the circles
                for circle in circles:
                    dx = pos[0] - circle['pos'][0]
                    dy = pos[1] - circle['pos'][1]
                    distance = math.sqrt(dx * dx + dy * dy)
                    if distance < circle['radius'] and circle['draw_circle']:
                        circle['draw_circle'] = False
                        if circle['ring_radius'] > 2*(circle['radius'] + circle['start_radius']) / 3:
                            if combo > max_combo:
                                max_combo = combo
                            combo=0
                            miss+=1
                            #print('miss')
                        elif circle['ring_radius'] > (circle['radius'] + circle['start_radius']) / 3:
                            score += 100 * combo
                            hits += 1
                            hit_sound.play()
                            #print("outer")

                        else:
                            score += 300 * combo
                            hits += 1
                            hit_sound.play()
                            #print('inner')
                        circle['ring_radius'] = 0  # Also hide the ring
                        combo +=1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_x:
                    pos = pygame.mouse.get_pos()
                    for circle in circles:
                        dx = pos[0] - circle['pos'][0]
                        dy = pos[1] - circle['pos'][1]
                        distance = math.sqrt(dx * dx + dy * dy)
                        if distance < circle['radius'] and circle['draw_circle']:
                            circle['draw_circle'] = False
                            if circle['ring_radius'] > 2 * (circle['radius'] + circle['start_radius']) / 3:
                                if combo > max_combo:
                                    max_combo = combo
                                combo = 0
                                miss += 1
                            elif circle['ring_radius'] > (circle['radius'] + circle['start_radius']) / 3:
                                score += 100 * combo
                                hits += 1
                                winsound.PlaySound(r'soft-hitsoft.wav',
                                                   winsound.SND_FILENAME)
                            else:
                                score += 300 * combo
                                hits += 1
                                winsound.PlaySound(r'soft-hitsoft.wav', winsound.SND_FILENAME)
                            circle['ring_radius'] = 0  # Also hide the ring
                            combo += 1
        screen.fill((0, 0, 0))  # Fill the screen with black

        for i, circle in enumerate(circles):
            # Delay before drawing the circle and its ring
            if pygame.time.get_ticks() < circle['start_time']:
                continue

            # Draw the main circle and its ring if the flag is set
            if circle['draw_circle']:
                pygame.draw.circle(screen, circle['color'], circle['pos'], circle['radius'])
                num = circle['local_num']
                text = font.render(str(num), True, (0, 0, 0))  # Render the number
                text_rect = text.get_rect(center=circle['pos'])  # Center the text
                screen.blit(text, text_rect)  # Draw the text

                # Draw the converging ring
                if circle['ring_radius'] > circle['radius']:
                    pygame.draw.circle(screen, circle['color'], circle['pos'], circle['ring_radius'], 2)
                    circle['ring_radius'] -= circle['speed']
                else:  # The ring has converged with the circle
                    # Set the convergence time
                    if pygame.time.get_ticks() >= circle['start_time'] + 500:  # Hardcoded to 500 milliseconds
                        circle['draw_circle'] = False
                        circle['ring_radius'] = 0  # Also hide the ring
                        if combo > max_combo:
                            max_combo = combo
                        combo = 1
                        miss+=1
                        print("combo break sound")  # Print a message

        pygame.display.flip()
        clock.tick(60)

        if (hits+miss == len(circles)):
            #finished = False
            if combo > max_combo:
                max_combo = combo
            return [score, max_combo, hits, miss]  # Return the score when the game ends
def random_circles(num):
    circles=[]
    past_x = 0
    past_y = 0
    local = 0
    color = False
    for i in range(num):
        if (i % 10 == 0):
            local = 0
            if color:
                color = False
            else:
                color = True
        local += 1
        xpos = random.randint(100, 1180)
        ypos = random.randint(100, 620)
        while (xpos > past_x - 30 and xpos < past_x + 30):
            xpos = random.randint(100, 1180)
        while (ypos > past_y - 30 and ypos < past_y + 30):
            ypos = random.randint(100, 620)
        # print(i, xpos, ypos)
        if color:
            circles.append(
                {'color': (255, 0, 0), 'pos': (xpos, ypos), 'radius': 40, 'ring_radius': 100, 'start_radius': 100,
                 'speed': 1, 'draw_circle': True, 'start_time': 500 + i * 400, 'local_num': local})
        else:
            circles.append(
                {'color': (0, 128, 0), 'pos': (xpos, ypos), 'radius': 40, 'ring_radius': 100, 'start_radius': 100,
                 'speed': 1, 'draw_circle': True, 'start_time': 500 + i * 400, 'local_num': local})
        past_x = xpos
        past_y = ypos
    return circles
def end_screen(info):
    screen.fill((0, 255, 0))  # Fill the screen with green
    font = pygame.font.Font(None, 72)  # Font for the game statistics
    text = font.render(f"Score: {info[0]}", True, (0, 0, 0))
    screen.blit(text, (200, 100))
    text = font.render(f"Max Combo: {info[1]}", True, (0, 0, 0))
    screen.blit(text, (200, 200))
    text = font.render(f"Hits: {info[2]} Misses: {info[3]}", True, (0, 0, 0))
    screen.blit(text, (200, 300))
    accuracy = info[2] / (info[2] + info[3]) * 100  # Calculate the accuracy
    text = font.render(f"Accuracy: {accuracy:.1f}%", True, (0, 0, 0))
    screen.blit(text, (200, 400))
    pygame.display.flip()
    time.sleep(10)

# Define your circles here
# circles = [
#     {'color': (255, 255, 255), 'pos': (400, 300), 'radius': 50, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 0},
#     {'color': (255, 255, 255), 'pos': (100, 100), 'radius': 50, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 1000},
#     {'color': (255, 255, 255), 'pos': (700, 100), 'radius': 50, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 2000},
#     {'color': (255, 255, 255), 'pos': (100, 500), 'radius': 50, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 3000},
#     {'color': (255, 255, 255), 'pos': (700, 500), 'radius': 50, 'ring_radius': 100, 'speed': 1, 'draw_circle': True, 'start_time': 4000}
# ]


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("purple")
    pygame.display.flip()
    circles = random_circles(20)
    info = draw_circles_with_converging_rings(screen, circles)
    end_screen(info)

    clock.tick(60)
pygame.quit()


print("DONE")

time.sleep(20)

#print("Score: "+str(info[0])+"\nMax Combo: "+str(info[1])+"\nHits: "+str(info[2])+" Misses: "+str(info[3])+"\nAccuracy: "+str(100 * (info[2]/(info[2]+info[3])))+"%")
