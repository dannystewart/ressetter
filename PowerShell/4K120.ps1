# Specify the resolution, color depth, and refresh rate
$width = 3840
$height = 2160
$colorDepth = 32
$refreshRate = 120

# Specify known path to nircmd.exe in case it's not on the system path
$nircmdPath = "C:\Users\danny\Developer\4k120\nircmd.exe"

try {
    $command = (Get-Command nircmd).Source
}
catch {
    $command = $nircmdPath
}

# Run nircmd.exe to set the display settings
$command = "$command setdisplay $width $height $colorDepth $refreshRate"
Invoke-Expression -Command $command
