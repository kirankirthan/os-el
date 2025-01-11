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
# Rest of your code (e.g., initialization, simulation logic)
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MRU Demand Paging Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Simulation settings
frames = [None, None, None]  # Example with 3 memory frames
# page_sequence = [1, 2, 3, 2, 4, 5, 1, 6, 3, 7]
page_faults = 0
font = pygame.font.Font(None, 36)

# Main loop
def simulation():
    global frames, page_faults
    clock = pygame.time.Clock()
    current_page_index = 0
    recent_usage = []  # To track the order of recent usage
    fault_indices = []  # To store the indices where page faults occurred

    while current_page_index < len(page_sequence):
        screen.fill(WHITE)
        page = page_sequence[current_page_index]

        # Display the reference string text on one line
        ref_text_line1 = "Reference String:"
        ref_render_line1 = font.render(ref_text_line1, True, BLACK)
        screen.blit(ref_render_line1, (50, 10))

        # Display the sequence of numbers (ref_text) on the next line
        ref_text_line2 = " ".join(map(str, page_sequence))
        ref_render_line2 = font.render(" " + ref_text_line2, True, BLACK)
        screen.blit(ref_render_line2, (50, 50))

        # Measure the width of each number in the reference string for alignment
        text_width = font.size("0")[0] + 6.8  # Approx. width of each character with spacing

        # Check if page is already in memory
        page_fault = False
        if page not in frames:
            page_faults += 1
            page_fault = True
            fault_indices.append(current_page_index)  # Store index of page fault

            if None in frames:
                # Replace an empty frame first
                empty_index = frames.index(None)
                frames[empty_index] = page
            else:
                # Use MRU to determine which page to replace
                mru_page = recent_usage.pop()  # Get the most recently used page
                mru_index = frames.index(mru_page)  # Find its index in the frames
                frames[mru_index] = page  # Replace it

        # Update recent usage list
        if page in recent_usage:
            recent_usage.remove(page)  # Remove if already in list
        recent_usage.append(page)  # Add to the end as most recently used

        # Draw memory frames
        for i, frame in enumerate(frames):
            color = GREEN if frame == page else BLACK
            pygame.draw.rect(screen, color, (200, 100 + i * 100, 100, 50))
            text = font.render(str(frame) if frame else "-", True, WHITE)
            screen.blit(text, (225, 110 + i * 100))

        # Display the current page being processed
        page_text = font.render(f"Current Page: {page}", True, RED)
        screen.blit(page_text, (400, 50))

        # Display the total page faults
        fault_text = font.render(f"Page Faults: {page_faults}", True, BLACK)
        screen.blit(fault_text, (400, 100))

        # Draw dots directly below the reference string for page faults
        for idx in fault_indices:
            dot_x = 50 + (idx * text_width) + 12  # Adjusted alignment for each number
            dot_y = 40  # Slightly below the reference string
            pygame.draw.circle(screen, RED, (dot_x, dot_y), 5)  # Draw a small red dot below

        pygame.display.flip()
        pygame.time.wait(5000)  # Wait for 1 second
        current_page_index += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Run simulation
simulation()