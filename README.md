# ResSetter

Simple utility to force a display resolution and refresh rate on Windows.

Originally created because my 120 Hz TV is stupid and would reset back to 60 Hz every time you turned it off. You can run this script and it'll do what it says on the tin: set the resolution and refresh rate to what you want.

You can use command line arguments to set a custom resolution or refresh rate:

- `--width` and `--height` for resolution
- `--refresh` for refresh rate

A cooler way to use it if you're suffering from a problem like mine is to use the `--background` argument, which will leave the script running and monitor for input (key presses or mouse movement). After a period of inactivity, when it detects input, it triggers the resolution and refresh rate change.

I couldn't get anything to reliably detect when the TV turned on or off, so instead I came up with this idea of resetting the resolution as soon as you (presumably) sit back down at the computer and wake it up. I've been using it for months and it's been rock solid.

You can also use arguments to specify the waiting period:
- `--timeout` sets the length of inactivity before new input will trigger a reset (in seconds)
- `--set-delay` will set the number of seconds after activity is detected before the reset will trigger

It will retry if it's unable to set the resolution at first:
- `--retry-delay` will set how long to wait before another retry (in seconds)
- `--max-retries` will set the max number of retries before it gives up

## Running the Script

```bash
pip install ressetter  # to install
ressetter  # to immediately set the resolution
ressetter --background  # to run the script in background mode
```

## Compiling the Script

If you want to turn the script into an EXE to run it more easily (e.g. on startup), you can do that with `pyinstaller` and the included spec file:

```bash
pyinstaller --noconfirm --clean --distpath=dist --workpath=build ressetter.spec
```

Then just take the compiled EXE, stick it somewhere accessible, and create a shortcut to it in your Start menu's Startup folder.

**Pro tip:** You can also set a shortcut key for it to something like `Ctrl+Alt+Shift+R` in Properties so you can invoke it without having to find and open it.
