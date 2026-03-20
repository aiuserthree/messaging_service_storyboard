# index.before-today.html — "며칠 전" 고정 스냅샷 (기본: 커밋 4944f63). 오늘 적용분 아님.
# 다른 커밋: .\save-before-today.ps1 abc1234
param(
    [string]$Commit = '4944f63'
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$lines = git show "${Commit}:index.html" 2>&1
if ($LASTEXITCODE -ne 0) { throw "git show failed for $Commit" }
$raw = if ($lines -is [array]) { $lines -join "`n" } else { [string]$lines }

$inject = "    <script src=`"js/index-version-switch.js`" defer></script>"
if ($raw -notmatch 'index-version-switch\.js') {
    $raw = $raw -replace '(?i)</body>', ($inject + "`n</body>")
}

$comment = "<!-- 비교용: 커밋 $Commit 시점 index.html. 갱신: .\save-before-today.ps1 -->" + "`n"
if ($raw -notmatch '비교용: 커밋') {
    $raw = $raw -replace '<!DOCTYPE html>', "<!DOCTYPE html>`n$comment"
}

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText((Join-Path $PWD 'index.before-today.html'), $raw, $utf8NoBom)
Write-Host "OK: index.before-today.html <- $Commit"
