# 마지막 커밋의 index.html -> index.last-commit.html 로 저장 (비교용)
# 버전 전환 바 스크립트는 HEAD에 없으면 자동 삽입
# 사용: .\save-index-snapshot.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$lines = git show HEAD:index.html 2>&1
if ($LASTEXITCODE -ne 0) { throw "git show failed" }
# PowerShell은 줄 배열로 받을 수 있음 -> 줄바꿈 유지
$raw = if ($lines -is [array]) { $lines -join "`n" } else { [string]$lines }

$inject = "    <script src=`"js/index-version-switch.js`" defer></script>"
if ($raw -notmatch 'index-version-switch\.js') {
    $raw = $raw -replace '(?i)</body>', ($inject + "`n</body>")
}

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText((Join-Path $PWD 'index.last-commit.html'), $raw, $utf8NoBom)
Write-Host "OK: index.last-commit.html 갱신됨 (HEAD 기준, 버전 바 자동 포함)"
