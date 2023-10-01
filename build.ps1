# Setup
$app_name="wordle_main.py"
$requirements=".\requirements.txt" # Create with pip freeze > pip_requirements.txt
$python_version=$(& python --version).split(' ').split('.')
$python_version_major_required=[int]"3"
$python_version_minor_required=[int]"10"

# Check Python is installed, otherwise abort
# convert major version and minor to int
$python_version_major=[int]$python_version[1]
$python_version_minor=[int]$python_version[2]
if ( $python_version_major -lt $python_version_major_required ) {
    Write-Output "Error: Python is either not detected or less than $($python_version_major_required).x"
    exit(1)
}
if ( $python_version_minor -lt $python_version_minor_required ){
    Write-Output "Error: Python is either not detected or less than $($python_version_major_required).$($python_version_minor_required)"
    exit(1)
}
Write-Output "Python $($python_version) detected - proceeding..."

# Create a venv (assumes python)
if (!(Test-Path .\.venv)){
    Write-Output "Create python venv.."
    & python.exe -m venv .venv
}else
{
    Write-Output "Detected .venv Skipping"
}
Write-Output "Install python requirements.."
& .\.venv\Scripts\pip.exe install -r $requirements

Write-Output "Remove Previous Versions"
if (Test-Path .\dist){
    Remove-Item .\dist -Recurse -Force
}

Write-Output "Building Application..."
& python.exe $path_to_build_util .\$app_name --onefile

# Check the Application built OK
if (Test-Path .\dist) {
    # Deploy files into dist folder
    Copy-Item .\game_assets .\dist -Recurse -Force
    # Deploy any extras defined earlier
    foreach ($file_type in $exta_files){
        Copy-Item $file_type .\dist\ -Force
    }
}
else {
    Write-Output "Error Failed to build application..."
}