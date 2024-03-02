import os
import subprocess
import sys

# Specify the resolution, color depth, and refresh rate
WIDTH = 3840
HEIGHT = 2160
COLOR_DEPTH = 32
REFRESH_RATE = 120


def print_colored(text, color, end="\n"):
    """Print text in the specified color."""
    try:
        from termcolor import colored
    except ImportError:
        print(text)

    print(colored(text, color), end=end)


def get_resource_path(relative_path):
    """Get the absolute path to a resource in a PyInstaller bundle."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def set_display(nircmd_path):
    """Set the display resolution and refresh rate using nircmd."""

    display_str = f"{WIDTH} {HEIGHT} {COLOR_DEPTH} {REFRESH_RATE}"
    command = f"{nircmd_path} setdisplay {display_str}"

    print_colored("Setting resolution to 4k120... ", "cyan", end="")

    subprocess.run(command, shell=True, check=True)

    print_colored("done!", "green")


def main():
    """Main function."""
    nircmd_path = get_resource_path("nircmd.exe")
    set_display(nircmd_path)


if __name__ == "__main__":
    main()
