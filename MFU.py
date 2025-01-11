import pygame
import sys


if len(sys.argv) > 3:  
    try:
        page_sequence = list(map(int, sys.argv[1].split(",")))
        num_frames = int(sys.argv[2])
        time_delay = int(sys.argv[3])  
    except ValueError:
        print("Invalid inputs. Ensure page sequence, frame count, and delay are valid.")
        sys.exit()

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MFU Demand Paging Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


frames = [None] * num_frames
page_faults = 0
font = pygame.font.Font(None, 36)

def simulation():
    global frames, page_faults
    clock = pygame.time.Clock()
    current_page_index = 0
    page_freq = {}  
    fault_indices = []  

    while current_page_index < len(page_sequence):
        screen.fill(WHITE)
        page = page_sequence[current_page_index]

        ref_text_line1 = "Reference String:"
        ref_render_line1 = font.render(ref_text_line1, True, BLACK)
        screen.blit(ref_render_line1, (50, 10))  

        ref_text_line2 = " ".join(map(str, page_sequence))
        ref_render_line2 = font.render(" "+ref_text_line2, True, BLACK)
        screen.blit(ref_render_line2, (50, 50))  

       
        text_width = font.size("0")[0]+6.8   
        
        if page in page_freq:
            page_freq[page] += 1
        else:
            page_freq[page] = 1

        if page not in frames:
            page_faults += 1
            fault_indices.append(current_page_index)

            if None in frames:
                empty_index = frames.index(None)
                frames[empty_index] = page
            else:
                mfu_page = max(frames, key=lambda p: page_freq.get(p, 0))  
                mfu_index = frames.index(mfu_page)  

                frames[mfu_index] = page

                page_freq[mfu_page] = 0

        for i, frame in enumerate(frames):
            color = GREEN if frame == page else BLACK
            pygame.draw.rect(screen, color, (200, 100 + i * 100, 100, 50))
            text = font.render(str(frame) if frame else "-", True, WHITE)
            screen.blit(text, (225, 110 + i * 100))

        page_text = font.render(f"Current Page: {page}", True, RED)
        screen.blit(page_text, (400, 50))

        fault_text = font.render(f"Page Faults: {page_faults}", True, BLACK)
        screen.blit(fault_text, (400, 100))

        for idx in fault_indices:
            dot_x = 50 + (idx * 20) + 12  
            dot_y = 80  
            pygame.draw.circle(screen, RED, (dot_x, dot_y), 5) 

        pygame.display.flip()
        pygame.time.wait(5000) 
        current_page_index += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

simulation()
