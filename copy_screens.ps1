$sourceDir = "c:\Users\abdul\.gemini\antigravity\scratch\Queue iq\Stitch_Screens"
$targetDir = "c:\Users\abdul\.gemini\antigravity\scratch\Queue iq\queueiq-app"

# Copy all HTML & WEBP
Copy-Item "$sourceDir\*.html" -Destination $targetDir -Force
Copy-Item "$sourceDir\*.webp" -Destination $targetDir -Force

# Rename main page to index.html
$oldIndex = Join-Path $targetDir "QR_Scan_Landing_Page.html"
$newIndex = Join-Path $targetDir "index.html"
if (Test-Path $oldIndex) {
    Move-Item $oldIndex $newIndex -Force
}
Write-Host "Files copied and renamed successfully."
