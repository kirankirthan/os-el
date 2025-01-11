import pygame
import sys




# Parse command-line arguments
if len(sys.argv) > 3:  # Expecting page sequence, frame count, and delay
    try:
        page_sequence = list(map(int, sys.argv[1].split(",")))
        num_frames = int(sys.argv[2])
        time_delay = int(sys.argv[3])  # Now this will work as expected
    except ValueError:
        print("Invalid inputs. Ensure page sequence, frame count, and delay are valid.")
        sys.exit()




pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FCFS Demand Paging Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize frames dynamically based on num_frames
frames = [None] * num_frames
page_faults = 0
font = pygame.font.Font(None, 36)

def simulation():
    global frames, page_faults
    clock = pygame.time.Clock()
    current_page_index = 0
    queue = []  
    fault_indices = []  

    while current_page_index < len(page_sequence):
        screen.fill(WHITE)
        page = page_sequence[current_page_index]

        # Draw reference string
        ref_text_line1 = "Reference String:"
        ref_render_line1 = font.render(ref_text_line1, True, BLACK)
        screen.blit(ref_render_line1, (50, 10)) 

        ref_text_line2 = " ".join(map(str, page_sequence))
        ref_render_line2 = font.render(" " + ref_text_line2, True, BLACK)
        screen.blit(ref_render_line2, (50, 50))  

        if page not in frames:
            page_faults += 1
            fault_indices.append(current_page_index)

            if None in frames:
                empty_index = frames.index(None)
                frames[empty_index] = page
                queue.append(page) 
            else:
                oldest_page = queue.pop(0)  
                oldest_index = frames.index(oldest_page)
                frames[oldest_index] = page  
                queue.append(page)  

        # Draw frames
        for i, frame in enumerate(frames):
            color = GREEN if frame == page else BLACK
            pygame.draw.rect(screen, color, (200, 100 + i * 100, 100, 50))
            text = font.render(str(frame) if frame else "-", True, WHITE)
            screen.blit(text, (225, 110 + i * 100))

        # Display page and faults
        page_text = font.render(f"Current Page: {page}", True, RED)
        screen.blit(page_text, (400, 50))
        fault_text = font.render(f"Page Faults: {page_faults}", True, BLACK)
        screen.blit(fault_text, (400, 100))

        # Highlight faults in reference string
        for idx in fault_indices:
            dot_x = 50 + (idx * 20) + 12  
            dot_y = 80 
            pygame.draw.circle(screen, RED, (dot_x, dot_y), 5)  

        pygame.display.flip()
        pygame.time.wait(time_delay)  # Use the specified delay
        current_page_index += 1

        # Quit event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

simulation()
