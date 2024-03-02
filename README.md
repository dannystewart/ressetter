# 4K120

Simple utility to force display resolution to 4K and refresh rate to 120 Hz, because my TV is stupid and it resets back to 60 Hz every damn time.

## How It Works

The script relies on the `setdisplay` function of [nircmd](https://www.nirsoft.net/utils/nircmd.html). It gets compiled into an EXE with PyInstaller (via `pycompiler.bat`) which bundles `nircmd.exe` to make one convenient double-clickable file.

### Note on Size

It uses `upx.exe` (the [Ultimate Packer for eXecutables](https://upx.github.io/)) to get a way-too-big 7 MB EXE file down to a still-too-big-but-a-little-better 5.8 MB EXE. Bundling the Python interpreter takes space, unfortunately. ☹️

## Tips

- **Pro tip:** Make a shortcut to 4K120.exe on your desktop, go into Properties, and set a shortcut key like Ctrl+Alt+Shift+R. This way you can invoke it without using the mouse.
