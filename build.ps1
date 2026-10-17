#requires -Version 5.1
<#
    一键打包 Unipus 复制内容解密工具。
    用法：powershell -ExecutionPolicy Bypass -File .\build.ps1
#>
param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if ($Clean) {
    foreach ($dir in @("build", "dist")) {
        $path = Join-Path $root $dir
        if (Test-Path -LiteralPath $path) {
            Remove-Item -LiteralPath $path -Recurse -Force
        }
    }
}

python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name "U_to_N" `
    --icon "$root\icon.ico" `
    --version-file "$root\version_info.txt" `
    --add-data "$root\web;web" `
    --hidden-import "webview.platforms.edgechromium" `
    --collect-all "webview" `
    --collect-all "clr_loader" `
    --collect-all "pythonnet" `
    "$root\app.py"

$built = Join-Path $root "dist\U_to_N.exe"
if (-not (Test-Path -LiteralPath $built)) {
    throw "构建失败：找不到 $built"
}

$release = Join-Path $root "dist\Unipus解密工具.exe"
Move-Item -LiteralPath $built -Destination $release -Force

Write-Host ""
Write-Host "构建完成：" -ForegroundColor Green
Write-Host "  $release"
Write-Host "文件大小：$([math]::Round((Get-Item -LiteralPath $release).Length / 1MB, 1)) MB"