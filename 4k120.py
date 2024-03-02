# pylint: disable=invalid-name

import subprocess

# Specify the resolution, color depth, and refresh rate
WIDTH = 3840
HEIGHT = 2160
COLOR_DEPTH = 32
REFRESH_RATE = 120

# Path to the nircmd.exe executable
NIRCMD_PATH = r"C:\Users\danny\OneDrive\Documents\Tech\Windows\nircmd-x64\nircmd.exe"


def main():
    """Main function"""
    command = f"{NIRCMD_PATH} setdisplay {WIDTH} {HEIGHT} {COLOR_DEPTH} {REFRESH_RATE}"
    print("Setting resolution to 4k120... ", end="")
    subprocess.run(command, shell=True)
    print("Done!")


if __name__ == "__main__":
    main()
