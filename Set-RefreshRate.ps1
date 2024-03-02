# Specify the resolution, color depth, and refresh rate
$width = 3840
$height = 2160
$colorDepth = 32
$refreshRate = 120

# Path to the nircmd.exe executable
$nircmdPath = "C:\Users\danny\OneDrive\Documents\Tech\Windows\nircmd-x64\nircmd.exe"

# Build the command to set the display settings
$command = "$nircmdPath setdisplay $width $height $colorDepth $refreshRate"

# Execute the command
Invoke-Expression -Command $command
