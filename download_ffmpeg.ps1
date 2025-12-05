# PowerShell script to download and extract FFmpeg
# This will be run during installation

param(
    [string]$InstallPath = "C:\Program Files\YouTube to MP3 Downloader\ffmpeg"
)

Write-Host "Downloading FFmpeg..."

# Create installation directory
New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null

# Download FFmpeg (using winget if available, otherwise direct download)
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$zipPath = Join-Path $env:TEMP "ffmpeg.zip"

try {
    # Try winget first (fastest)
    $wingetPath = Get-Command winget -ErrorAction SilentlyContinue
    if ($wingetPath) {
        Write-Host "Installing FFmpeg via winget..."
        & winget install --id=Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements --silent
        if ($LASTEXITCODE -eq 0) {
            Write-Host "FFmpeg installed successfully via winget"
            return
        }
    }
    
    # Fallback: Download and extract
    Write-Host "Downloading FFmpeg from official source..."
    Invoke-WebRequest -Uri $ffmpegUrl -OutFile $zipPath -UseBasicParsing
    
    Write-Host "Extracting FFmpeg..."
    Expand-Archive -Path $zipPath -DestinationPath $env:TEMP -Force
    
    # Find the extracted folder
    $extractedFolder = Get-ChildItem -Path $env:TEMP -Filter "ffmpeg-*-essentials*" -Directory | Select-Object -First 1
    
    if ($extractedFolder) {
        # Copy bin folder to installation path
        Copy-Item -Path (Join-Path $extractedFolder.FullName "bin\*") -Destination $InstallPath -Recurse -Force
        
        # Add to PATH for current session
        $env:Path += ";$InstallPath"
        
        Write-Host "FFmpeg extracted to: $InstallPath"
        
        # Cleanup
        Remove-Item $zipPath -ErrorAction SilentlyContinue
        Remove-Item $extractedFolder.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "FFmpeg installation failed. Please install manually."
    exit 1
}


