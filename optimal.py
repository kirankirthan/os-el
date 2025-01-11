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
pygame.display.set_caption("Optimal Demand Paging with FCFS on Tie Simulation")

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
def optimal():
    global frames, page_faults
    clock = pygame.time.Clock()
    current_page_index = 0
    fault_indices = []  # To store the indices where page faults occurred

    # Queue to remember the order pages were added (used for FCFS tie-breaking)
    page_queue = []

    while current_page_index < len(page_sequence):
        screen.fill(WHITE)
        page = page_sequence[current_page_index]
        
        # Display the reference string text on one line
        ref_text_line1 = "Reference String:"
        ref_render_line1 = font.render(ref_text_line1, True, BLACK)
        screen.blit(ref_render_line1, (50, 10))  # Position the first line at the top

        # Display the sequence of numbers (ref_text) on the next line
        ref_text_line2 = " ".join(map(str, page_sequence))
        ref_render_line2 = font.render(" "+ref_text_line2, True, BLACK)
        screen.blit(ref_render_line2, (50, 50))  # Position the second line below the first line

        # Measure the width of each number in the reference string for alignment
        text_width = font.size("0")[0] + 6.8  # Approx. width of each character with spacing

        # Check if page is already in memory
        if page not in frames:
            page_faults += 1
            fault_indices.append(current_page_index)

            # If there's space, add the page to an empty frame
            if None in frames:
                empty_index = frames.index(None)
                frames[empty_index] = page
                page_queue.append(page)  # Add to the queue (FCFS)
            else:
                # If no space, find the page to replace using the Optimal algorithm with FCFS on ties
                future_uses = []
                for frame in frames:
                    if frame not in page_sequence[current_page_index:]:
                        # If the page will not be used in the future, replace it
                        future_uses.append((frame, float('inf')))
                    else:
                        # Otherwise, calculate when the page will be used next
                        future_uses.append((frame, page_sequence[current_page_index:].index(frame) + current_page_index))

                # Check if there are pages with "infinity" next use (pages that aren't referenced again)
                infinity_pages = [frame for frame, future in future_uses if future == float('inf')]

                if len(infinity_pages) > 1:
                    # If there are multiple pages with no future use, apply FCFS logic
                    page_to_replace = page_queue.pop(0)  # Replace the first inserted page
                else:
                    # Otherwise, use Optimal: Replace the page with the furthest next use
                    max_future_use = max(future_uses, key=lambda x: x[1])[1]
                    candidates = [frame for frame, future in future_uses if future == max_future_use]
                    page_to_replace = candidates[0]  # No tie in this case

                # Replace the page
                if page_to_replace in frames:
                    page_index = frames.index(page_to_replace)
                    frames[page_index] = page  # Replace it with the new page
                else:
                    print(f"Error: {page_to_replace} not found in frames. This should not happen.")
                    continue  # Skip replacing if page is not found in frames

                page_queue.append(page)  # Add to the queue (FCFS)

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
            dot_x = 50 + (idx * 20) + 12  # Adjusted alignment for each number
            dot_y = 80  # Slightly below the reference string
            pygame.draw.circle(screen, RED, (dot_x, dot_y), 5)  # Draw a small red dot below

        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 1 second
        current_page_index += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Run simulation
optimal()
