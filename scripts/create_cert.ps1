<#
.SYNOPSIS
    Generate a self-signed code signing certificate for DevInstaller.
.DESCRIPTION
    Creates a self-signed certificate and exports it as a PFX file.
    The PFX should be base64-encoded and stored as a GitHub Actions secret.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\create_cert.ps1
#>

$CertName   = "DevInstaller Code Signing"
$Publisher   = "CN=faizanfatmi, O=DevInstaller, L=GitHub"
$ScriptDir  = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$RootDir    = Split-Path -Parent $ScriptDir
$OutputDir  = Join-Path $RootDir "build"
$PfxPath    = Join-Path $OutputDir "code_signing.pfx"

# Create output dir
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null }

# Prompt for PFX password
$Password = Read-Host -Prompt "Enter a password for the PFX file" -AsSecureString

# Create the self-signed certificate
$Cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject $Publisher `
    -FriendlyName $CertName `
    -CertStoreLocation Cert:\CurrentUser\My `
    -NotAfter (Get-Date).AddYears(3) `
    -KeyUsage DigitalSignature `
    -KeyAlgorithm RSA `
    -KeyLength 2048 `
    -HashAlgorithm SHA256

Write-Host "`nCertificate created: $($Cert.Thumbprint)" -ForegroundColor Green

# Export to PFX
Export-PfxCertificate -Cert $Cert -FilePath $PfxPath -Password $Password | Out-Null
Write-Host "Exported to: $PfxPath" -ForegroundColor Green

# Base64 encode for GitHub secrets
$Base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($PfxPath))
$B64Path = Join-Path $OutputDir "code_signing_base64.txt"
Set-Content -Path $B64Path -Value $Base64

Write-Host "`n===== SETUP INSTRUCTIONS =====" -ForegroundColor Cyan
Write-Host "1. Go to your GitHub repo -> Settings -> Secrets and variables -> Actions"
Write-Host "2. Add these repository secrets:"
Write-Host "   SIGN_CERT_PFX  = contents of $B64Path" -ForegroundColor Yellow
Write-Host "   SIGN_CERT_PASS = the password you just entered" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Delete $PfxPath and $B64Path after uploading (don't commit them!)" -ForegroundColor Red
Write-Host "===============================" -ForegroundColor Cyan

# Clean up cert from store (optional — keep if you want to sign locally too)
# Remove-Item "Cert:\CurrentUser\My\$($Cert.Thumbprint)" -Force
