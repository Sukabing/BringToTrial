# Run the hover regression case: copy the testcase into game/, run it, remove it again.
$ErrorActionPreference = "Stop"
$proj = "E:\Projects\RenPy\BringToTrial-Demo"
$sdk = "E:\Apps\renpy-8.5.3-sdk"

Copy-Item (Join-Path $proj "_hoverprobe.rpy") (Join-Path $proj "game\_hoverprobe.rpy") -Force
try {
    & "$sdk\lib\py3-windows-x86_64\python.exe" "$sdk\renpy.py" $proj test hover_probe 2>&1 |
        Select-String -Pattern "PROBE|Status|passed|failed|rror|Assertion" | ForEach-Object { $_.Line }
}
finally {
    Remove-Item (Join-Path $proj "game\_hoverprobe.rpy"), (Join-Path $proj "game\_hoverprobe.rpyc") -Force -ErrorAction SilentlyContinue
}
