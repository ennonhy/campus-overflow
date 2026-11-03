<#
.SYNOPSIS
    把 Lab 2 产出物按规范路径拷进团队仓库克隆目录，并打印后续 git 命令。

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\copy_to_repo.ps1 -RepoPath "D:\code\campus-overflow-team3"
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,
    [string]$Branch = "feature/lab2-backlog"
)

$ErrorActionPreference = 'Stop'

$src = Join-Path $PSScriptRoot '..\docs'
if (-not (Test-Path $src)) { throw "找不到源目录：$src" }
if (-not (Test-Path $RepoPath)) { throw "仓库目录不存在：$RepoPath" }
if (-not (Test-Path (Join-Path $RepoPath '.git'))) { throw "这不是 git 仓库（没有 .git 目录）：$RepoPath" }

$dest = Join-Path $RepoPath 'docs\backlog'
New-Item -ItemType Directory -Force -Path (Join-Path $dest 'stories') | Out-Null
$dest = (Resolve-Path $dest).Path

Copy-Item -Path (Join-Path $src 'backlog\*') -Destination $dest -Recurse -Force

$tools = Join-Path $src '..\tools'
if (Test-Path $tools) {
    Copy-Item -Path $tools -Destination (Join-Path $RepoPath 'tools') -Recurse -Force
}

Write-Host ""
Write-Host "=== 已拷入 $dest ===" -ForegroundColor Green
Get-ChildItem $dest -Recurse -File | ForEach-Object {
    Write-Host ("  {0,-20} {1,8:N1} KB" -f $_.FullName.Substring($dest.Length + 1), ($_.Length / 1KB))
}

$feature = (Get-ChildItem (Join-Path $dest 'stories') -Filter *.feature -ErrorAction SilentlyContinue).Count
if ($feature -ge 8) {
    Write-Host ""
    Write-Host ".feature 文件数：$feature （满足 >= 8 的要求）" -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host ".feature 文件数：$feature （不足 8，请检查 stories 目录）" -ForegroundColor Red
}

Push-Location $RepoPath
try {
    Write-Host ""
    Write-Host "=== git 状态（应只出现 docs/backlog 与 tools）===" -ForegroundColor Cyan
    git status --short

    Write-Host ""
    Write-Host "下一步（逐条复制执行）：" -ForegroundColor Yellow
    Write-Host "  git checkout main"
    Write-Host "  git pull origin main"
    Write-Host "  git checkout -b $Branch"
    Write-Host "  git add docs/backlog"
    Write-Host '  git commit -m "docs(backlog): Lab2 需求建模产出——故事地图/Backlog/Gherkin/Sprint1 计划"'
    Write-Host "  git push -u origin $Branch"
    Write-Host ""
    Write-Host "推送后到 GitHub 点 Create a pull request，描述粘贴 lab2-submission/PR-body.md" -ForegroundColor Yellow
}
finally {
    Pop-Location
}
