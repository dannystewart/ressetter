import subprocess

# Specify the resolution, color depth, and refresh rate
WIDTH = 3840
HEIGHT = 2160
COLOR_DEPTH = 32
REFRESH_RATE = 120

# Path to the nircmd.exe executable
NIRCMD_PATH = r"C:\Users\danny\OneDrive\Documents\Tech\Windows\nircmd-x64\nircmd.exe"


def check_for_nircmd():
    """Check if nircmd is accessible from the system's PATH."""
    try:
        subprocess.run(
            ["nircmd", "wait", "1"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    """Main function."""
    nircmd_path = "nircmd" if check_for_nircmd() else NIRCMD_PATH
    command = f"{nircmd_path} setdisplay {WIDTH} {HEIGHT} {COLOR_DEPTH} {REFRESH_RATE}"
    print("Setting resolution to 4k120... ", end="")
    subprocess.run(command, shell=True)
    print("Done!")


if __name__ == "__main__":
    main()
