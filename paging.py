import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paging Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 36)

logical_address_bits = 10
page_bits = 4  
offset_bits = logical_address_bits - page_bits

def generate_logical_address():
    return format(random.randint(0, 2**logical_address_bits - 1), f'0{logical_address_bits}b')

def get_page_offset(logical_address):
    page = int(logical_address[:page_bits], 2)
    offset = int(logical_address[page_bits:], 2)
    return page, offset

def initialize_simulation(num_pages, num_frames):
    page_table = [{"frame": None, "valid": False} for _ in range(num_pages)]
    memory_frames = [None] * num_frames

    for i in range(min(num_pages, num_frames)):
        frame = i
        page_table[i]["frame"] = frame
        page_table[i]["valid"] = True
        memory_frames[frame] = i

    return page_table, memory_frames

def draw_cpu_and_address(logical_address, page, offset):
    pygame.draw.rect(screen, GRAY, (50, 100, 150, 100))
    cpu_text = font.render("CPU", True, BLACK)
    screen.blit(cpu_text, (100, 130))

    pygame.draw.rect(screen, GRAY, (250, 100, 300, 50))
    la_text = font.render(f"Logical Address: {logical_address}", True, BLACK)
    screen.blit(la_text, (260, 115))

    po_text = font.render(f"Page: {page}, Offset: {offset}", True, BLACK)
    screen.blit(po_text, (260, 160))

def draw_physical_address(physical_address, page_fault):
    color = RED if page_fault else GREEN
    pygame.draw.rect(screen, GRAY, (250, 200, 300, 50))
    
    if page_fault:
        pa_text = font.render("Physical Address: Page Fault", True, BLACK)
    else:
        pa_text = font.render(f"Physical Address: {physical_address}", True, BLACK)
    
    screen.blit(pa_text, (260, 215))


def draw_page_table(page_table):
    start_x, start_y = 600, 100
    cell_width, cell_height = 120, 40

    headers = ["Page", "Frame", "Valid"]
    for i, header in enumerate(headers):
        text = font.render(header, True, BLACK)
        screen.blit(text, (start_x + i * cell_width, start_y - 40))

    for i, entry in enumerate(page_table):
        text = font.render(str(i), True, BLACK)
        screen.blit(text, (start_x, start_y + i * cell_height))
        frame_text = str(entry["frame"]) if entry["frame"] is not None else "-"
        text = font.render(frame_text, True, BLACK)
        screen.blit(text, (start_x + cell_width, start_y + i * cell_height))
        valid_text = "1" if entry["valid"] else "0"
        text = font.render(valid_text, True, BLACK)
        screen.blit(text, (start_x + 2 * cell_width, start_y + i * cell_height))

def draw_physical_memory(memory_frames):
    start_x, start_y = 1000, 100
    cell_width, cell_height = 120, 40

    text = font.render("Physical Memory", True, BLACK)
    screen.blit(text, (start_x, start_y - 40))

    for i, frame in enumerate(memory_frames):
        rect = pygame.Rect(start_x, start_y + i * cell_height, cell_width, cell_height)
        pygame.draw.rect(screen, BLUE, rect, 2)
        frame_text = str(frame) if frame is not None else "-"
        text = font.render(frame_text, True, BLACK)
        screen.blit(text, (start_x + 10, start_y + i * cell_height + 10))

def draw_arrows():
    pygame.draw.line(screen, BLACK, (200, 150), (250, 125), 2)  # CPU to Logical Address
    pygame.draw.line(screen, BLACK, (550, 125), (600, 125), 2)  # Logical Address to Page Table
    pygame.draw.line(screen, BLACK, (850, 125), (1000, 125), 2)  # Page Table to Physical Memory

def simulation_step(page_table, memory_frames, logical_address):
    page, offset = get_page_offset(logical_address)
    valid = page_table[page]["valid"]
    frame = page_table[page]["frame"] if valid else None
    physical_address = None
    page_fault = not valid

    if valid:
        physical_address = (frame << offset_bits) + offset

    return page, offset, frame, valid, physical_address, page_fault

def main():
    running = True
    num_pages = 16
    num_frames = 8

    page_table, memory_frames = initialize_simulation(num_pages, num_frames)

    while running:
        screen.fill(WHITE)

        logical_address = generate_logical_address()
        page, offset, frame, valid, physical_address, page_fault = simulation_step(
            page_table, memory_frames, logical_address
        )

        title = large_font.render("Paging Simulation", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 100, 20))

        draw_cpu_and_address(logical_address, page, offset)
        draw_physical_address(physical_address, page_fault)
        draw_page_table(page_table)
        draw_physical_memory(memory_frames)
        draw_arrows()


        
        result_text = f" (Page Fault: {'Yes' if page_fault else 'No'})"
        text = font.render(result_text, True, RED if page_fault else GREEN)
        screen.blit(text, (50, 600))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        pygame.time.wait(3000)  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
