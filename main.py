import pygame
import sys
import subprocess

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demand Paging Simulation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

ALGORITHM_FILES = {
    
    "LRU": r"C:\Users\kiran\Desktop\os el\LRU.py",
    "LFU": r"C:\Users\kiran\Desktop\os el\LFU.py",
    "MRU": r"C:\Users\kiran\Desktop\os el\MRU.py",
    "MFU": r"C:\Users\kiran\Desktop\os el\MFU.py",
    "FCFS": r"C:\Users\kiran\Desktop\os el\FCFS.py",
    "Optimal": r"C:\Users\kiran\Desktop\os el\Optimal.py",
}

def run_algorithm(file_path, page_sequence, time_delay, num_frames):
    """
    Execute the algorithm located at the given file path using subprocess.
    """
    try:
        # Pass the page sequence, time delay, and number of frames as command-line arguments
        subprocess.run([
            "python", file_path,
            ",".join(map(str, page_sequence)),
             str(time_delay),str(num_frames)
        ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {file_path}: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")

def get_inputs():
    """
    Allow the user to input a custom page sequence, time delay, and number of frames.
    """
    input_box = pygame.Rect(100, 300, 600, 40)
    user_text = ""
    active = False
    prompt_index = 0

    inputs = ["Page Sequence (comma-separated)", "Time Delay (seconds)", "Number of Frames"]
    results = []

    while prompt_index < len(inputs):
        screen.fill(WHITE)
        
        prompt = font.render(f"Enter {inputs[prompt_index]}:", True, BLACK)
        screen.blit(prompt, (100, 250))

        pygame.draw.rect(screen, BLACK if active else GREEN, input_box, 2)
        text_surface = font.render(user_text, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if prompt_index == 0:  # Page sequence
                            try:
                                results.append(list(map(int, user_text.split(","))))
                            except ValueError:
                                print("Invalid input. Please enter numbers separated by commas.")
                                user_text = ""
                                continue
                        else:  # Time delay and number of frames
                            try:
                                results.append(float(user_text) if prompt_index == 1 else int(user_text))
                            except ValueError:
                                print("Invalid input. Please enter a valid number.")
                                user_text = ""
                                continue

                        prompt_index += 1
                        user_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        pygame.display.flip()

    return results

def main_menu():
    """
    Display the main menu for algorithm selection and page sequence input.
    """
    running = True
    selected_algorithm = None

    while running:
        screen.fill(WHITE)
        title = font.render("Demand Paging Simulation", True, BLACK)
        screen.blit(title, (250, 50))

        algo_text = font.render(
            "Select Algorithm: (1) FCFS (2) LRU (3) LFU (4) MRU (5) MFU  (6) Optimal",
            True,
            BLACK,
        )
        screen.blit(algo_text, (50, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_algorithm = "FCFS"
                    running = False
                elif event.key == pygame.K_2:
                    selected_algorithm = "LRU"
                    running = False
                elif event.key == pygame.K_3:
                    selected_algorithm = "LFU"
                    running = False
                elif event.key == pygame.K_4:
                    selected_algorithm = "MRU"
                    running = False
                elif event.key == pygame.K_5:
                    selected_algorithm = "MFU"
                    running = False
                elif event.key == pygame.K_6:
                    selected_algorithm = "Optimal"
                    running = False

        pygame.display.flip()

    page_sequence, time_delay, num_frames = get_inputs()

    if selected_algorithm:
        run_algorithm(ALGORITHM_FILES[selected_algorithm], page_sequence, num_frames, int(time_delay * 1000))

if __name__ == "__main__":
    main_menu()
