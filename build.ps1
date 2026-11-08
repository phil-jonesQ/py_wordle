if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv is required to build this project."
    exit 1
}

Write-Output "Install project and build dependencies..."
& uv sync --group build --locked
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Output "Remove Previous Versions"
if (Test-Path .\dist){
    Remove-Item .\dist -Recurse -Force
}

Write-Output "Building Application..."
& uv run --locked --group build pyinstaller .\py_wordle.py --onefile --name wordle_main --add-data "$PSScriptRoot\wordlist.txt;." --add-data "$PSScriptRoot\guess_words.txt;."
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

# Check the Application built OK
if (Test-Path .\dist) {
    # Deploy files into dist folder
    Copy-Item .\game_assets .\dist -Recurse -Force
}
else {
    Write-Error "Failed to build application."
    exit 1
}
