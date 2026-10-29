# Copy the project to a temp dir, fill silent placeholder audio, run the playthrough testcase.
$ErrorActionPreference = "Stop"
$src = "E:\Projects\RenPy\Bring To Trial"
$dst = Join-Path $env:TEMP "btt_full_test"
$sdk = "E:\Apps\renpy-8.5.3-sdk"
$ff = "C:\Users\sukab\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"

if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
New-Item -ItemType Directory -Path $dst -Force | Out-Null
Copy-Item "$src\project.json" -Destination $dst
Copy-Item "$src\game" -Destination "$dst\game" -Recurse
Remove-Item "$dst\game\saves", "$dst\game\cache" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$dst\game\script.rpy.orig" -Force -ErrorAction SilentlyContinue

$silence = Join-Path $dst "game\_silence.ogg"
& $ff -y -hide_banner -loglevel error -f lavfi -i "anullsrc=r=44100:cl=mono" -t 0.3 -c:a libvorbis -q:a 1 $silence
if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed" }

$script = Get-Content (Join-Path $dst "game\script.rpy") -Raw
$names = [regex]::Matches($script, '(?:voice|music) "([^"]+\.ogg)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
foreach ($n in $names) { Copy-Item $silence (Join-Path $dst "game\$n") -Force }
Write-Output ("placeholder ogg: " + $names.Count)

Copy-Item (Join-Path $src "_playthrough.rpy") (Join-Path $dst "game\_playthrough.rpy")
& "$sdk\lib\py3-windows-x86_64\python.exe" "$sdk\renpy.py" $dst test full_playthrough 2>&1 |
    Select-String -Pattern "Status|passed|failed|Error|Exception" | ForEach-Object { $_.Line }
