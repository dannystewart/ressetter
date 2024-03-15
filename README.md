# 4K120

Simple utility to force display resolution to 4K and refresh rate to 120 Hz, because my TV is stupid and it resets back to 60 Hz every damn time.

## How It Works

The script uses `pywin32` to set Windows display settings. It gets compiled into an EXE with PyInstaller (via `pycompiler.bat`) to make a convenient double-clickable file.

It uses `upx.exe` (the [Ultimate Packer for eXecutables](https://upx.github.io/)) to get the 7 MB EXE file down to about 5.8 MB. Bundling the Python interpreter takes space, unfortunately. ☹️

## Tips

- **Pro tip:** Make a shortcut to `4K120.exe` on your desktop and set a shortcut key like `Ctrl+Alt+Shift+R` in Properties so you can invoke it without using the mouse.
