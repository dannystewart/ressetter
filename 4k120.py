import subprocess

# Specify the resolution, color depth, and refresh rate
WIDTH = 3840
HEIGHT = 2160
COLOR_DEPTH = 32
REFRESH_RATE = 120

# Path to the nircmd.exe executable
NIRCMD_PATH = r"C:\Users\danny\OneDrive\Documents\Tech\Windows\nircmd-x64\nircmd.exe"


def set_display(nircmd_path):
    """Set the display resolution and refresh rate using nircmd."""
    command = f"{nircmd_path} setdisplay {WIDTH} {HEIGHT} {COLOR_DEPTH} {REFRESH_RATE}"
    print("Setting resolution to 4k120... ", end="")
    subprocess.run(command, shell=True, check=True)
    print("Done!")


def main():
    """Main function."""
    try:
        # Try to use nircmd from the system PATH
        set_display("nircmd")
    except subprocess.CalledProcessError:
        # If the command fails, use the fallback path
        set_display(NIRCMD_PATH)


if __name__ == "__main__":
    main()
