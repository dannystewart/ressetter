import subprocess

# Specify the resolution, color depth, and refresh rate
WIDTH = 3840
HEIGHT = 2160
COLOR_DEPTH = 32
REFRESH_RATE = 120

# Path to the nircmd.exe executable
NIRCMD_PATH = r"C:\Users\danny\OneDrive\Documents\Tech\Windows\nircmd-x64\nircmd.exe"


def print_colored(text, color, end="\n"):
    """Print text in the specified color."""
    try:
        from termcolor import colored
    except ImportError:
        print(text)

    print(colored(text, color), end=end)


def set_display(nircmd_path):
    """Set the display resolution and refresh rate using nircmd."""

    display_str = f"{WIDTH} {HEIGHT} {COLOR_DEPTH} {REFRESH_RATE}"
    command = f"{nircmd_path} setdisplay {display_str}"

    print_colored("Setting resolution to 4k120... ", "cyan", end="")

    subprocess.run(command, shell=True, check=True)

    print_colored("done!", "green")


def main():
    """Main function."""
    try:  # Try to use nircmd from the system PATH
        set_display("nircmd")
    except subprocess.CalledProcessError:  # If not, use fallback path
        set_display(NIRCMD_PATH)


if __name__ == "__main__":
    main()
