# 把打包好的 BringToTrial-1.0-pc.zip 发到 GitHub Releases
#
# 用法（默认建「草稿」发行版，网页上点一下就公开）：
#   pwsh -File "E:\Projects\RenPy\_github_release.ps1"
#   pwsh -File "E:\Projects\RenPy\_github_release.ps1" -Publish        # 建完立刻公开
#   pwsh -File "E:\Projects\RenPy\_github_release.ps1" -Private        # 仓库建成私有
#
# 凭据从 Git Credential Manager 里取（git push 用的那份），不落盘、不回显。

param(
    [string]$Owner = "Sukabing",
    [string]$Repo = "BringToTrial",
    [string]$Tag = "v1.0",
    [string]$Zip = "E:\Projects\RenPy\BringToTrial-1.0-dists\BringToTrial-1.0-pc.zip",
    [string]$Notes = "E:\Projects\RenPy\RELEASE-NOTES-v1.0.md",
    [string]$RepoDir = "E:\Projects\RenPy",
    [switch]$Publish,
    [switch]$Private
)

# git 把进度和 "No such remote" 都写在 stderr 上，严格模式会当成致命错误，这里放宽，
# 每一步自己看 $LASTEXITCODE。
$ErrorActionPreference = "Continue"
$env:GIT_TERMINAL_PROMPT = "0"

function Get-Token {
    $raw = ("protocol=https`nhost=github.com`nusername=$Owner`n`n" | git credential fill 2>$null | Out-String)
    $tok = (($raw -split "`n") | Where-Object { $_ -match '^password=' }) -replace '^password=', ''
    $tok = $tok.Trim()
    if (-not $tok) { throw "Git Credential Manager 里没有 github.com 的凭据，先跑一次 git push 让它存下来" }
    return $tok
}

$token = Get-Token
$api = @{
    Authorization          = "token $token"
    'User-Agent'           = 'BringToTrial-release'
    Accept                 = 'application/vnd.github+json'
    'X-GitHub-Api-Version' = '2022-11-28'
}

# ---- 1. 仓库 ----
try {
    $null = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $api -Method Get
    Write-Host "[1/4] 仓库已存在：$Owner/$Repo"
} catch {
    if ($_.Exception.Response.StatusCode.value__ -ne 404) { throw }
    $body = @{
        name        = $Repo
        description = "Bring To Trial / 三审少年 —— Ren'Py 互动小说"
        private     = [bool]$Private
        has_issues  = $true
        has_wiki    = $false
    } | ConvertTo-Json
    $null = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $api -Method Post `
        -Body ([Text.Encoding]::UTF8.GetBytes($body)) -ContentType 'application/json; charset=utf-8'
    Write-Host "[1/4] 已新建仓库：$Owner/$Repo（private=$([bool]$Private)）"
}

# ---- 2. 推送 main + 标签 ----
Push-Location $RepoDir
try {
    $remoteUrl = "https://github.com/$Owner/$Repo.git"
    $existing = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        git remote add origin $remoteUrl
    } elseif ($existing -ne $remoteUrl) {
        git remote set-url origin $remoteUrl
    }
    git push -u origin main
    if ($LASTEXITCODE -ne 0) { throw "git push 失败" }
    if (-not (git tag -l $Tag)) { git tag -a $Tag -m "Bring To Trial $Tag" }
    git push origin $Tag
    if ($LASTEXITCODE -ne 0) { throw "git push tag 失败" }
    Write-Host "[2/4] main 与 $Tag 已推送"
} finally {
    Pop-Location
}

# ---- 3. 发行版 ----
$release = $null
try {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/releases/tags/$Tag" -Headers $api
    Write-Host "[3/4] 发行版 $Tag 已存在"
} catch {
    if ($_.Exception.Response.StatusCode.value__ -ne 404) { throw }
    $body = @{
        tag_name   = $Tag
        name       = "Bring To Trial $Tag"
        body       = [IO.File]::ReadAllText($Notes, [Text.Encoding]::UTF8)
        draft      = (-not $Publish)
        prerelease = $false
    } | ConvertTo-Json -Depth 3
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/releases" -Headers $api -Method Post `
        -Body ([Text.Encoding]::UTF8.GetBytes($body)) -ContentType 'application/json; charset=utf-8'
    Write-Host "[3/4] 已建发行版 $Tag（draft=$(-not $Publish)）"
}

# ---- 4. 传包 ----
if (-not $release) { throw "发行版没建成，后面的上传跳过" }
$assetName = Split-Path $Zip -Leaf
$hasAsset = $false
foreach ($a in (Invoke-RestMethod -Uri $release.assets_url -Headers $api)) {
    if ($a.name -eq $assetName) { $hasAsset = $true }
}
if ($hasAsset) {
    Write-Host "[4/4] 附件 $assetName 已存在，跳过"
} else {
    $uploadUrl = ($release.upload_url -replace '\{.*$', '') + "?name=$assetName"
    $upHeaders = @{
        Authorization = "token $token"
        'User-Agent'  = 'BringToTrial-release'
        Accept        = 'application/vnd.github+json'
    }
    $resp = Invoke-RestMethod -Uri $uploadUrl -Headers $upHeaders -Method Post `
        -InFile $Zip -ContentType 'application/zip' -TimeoutSec 3600
    Write-Host ("[4/4] 已上传 {0}（{1:N1} MB）" -f $resp.name, ($resp.size / 1MB))
}

Write-Host "完成：$($release.html_url)"
if (-not $Publish) { Write-Host "（草稿状态，去网页点 Publish release 才会公开）" }
