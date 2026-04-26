import os
import time

class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_header(title, width=50, color=Colors.CYAN):
    """Generates a uniform, structured header for all menus."""
    print(f"\n{color}╔{'═' * (width - 2)}╗{Colors.RESET}")
    print(f"{color}║{Colors.RESET} {Colors.BOLD}{title.center(width - 4)}{Colors.RESET} {color}║{Colors.RESET}")
    print(f"{color}╚{'═' * (width - 2)}╝{Colors.RESET}")

def loading(message, duration=1.5):
    """Clean loading animation."""
    print(f"{Colors.CYAN}{message}{Colors.RESET}", end="")
    for _ in range(3):
        time.sleep(duration / 3)
        print(".", end="", flush=True)
    print("\n")

def pause():
    input(f"\n{Colors.GREEN}Appuyez sur Entrée pour continuer...{Colors.RESET}")