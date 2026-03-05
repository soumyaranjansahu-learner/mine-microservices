# setup.ps1

Write-Host "Setting up MINE Microservices Super App..."

# Ensure we are in the project root
$ProjectRoot = "c:\Users\dm2so\Desktop\Mine-Project"
Set-Location $ProjectRoot

# Create Virtual Environment if it doesn't exist
if (-not (Test-Path "$ProjectRoot\venv")) {
    Write-Host "Creating Virtual Environment..."
    python -m venv venv
}

# Activate Virtual Environment
Write-Host "Activating Virtual Environment..."
& "$ProjectRoot\venv\Scripts\Activate.ps1"

# Install Requirements
Write-Host "Installing Requirements from requirements.txt..."
pip install -r requirements.txt

# Create Main Gateway
if (-not (Test-Path "$ProjectRoot\mine_main")) {
    Write-Host "Creating Main Gateway..."
    django-admin startproject mine_main
    cd mine_main
    python manage.py startapp gateway
    cd ..
}

# Create Kitchen Microservice
if (-not (Test-Path "$ProjectRoot\mine_kitchen")) {
    Write-Host "Creating Kitchen Microservice..."
    django-admin startproject mine_kitchen
    cd mine_kitchen
    python manage.py startapp kitchen
    cd ..
}

# Create Shop Microservice
if (-not (Test-Path "$ProjectRoot\mine_shop")) {
    Write-Host "Creating Shop Microservice..."
    django-admin startproject mine_shop
    cd mine_shop
    python manage.py startapp shop
    cd ..
}

# Create Music Microservice
if (-not (Test-Path "$ProjectRoot\mine_music")) {
    Write-Host "Creating Music Microservice..."
    django-admin startproject mine_music
    cd mine_music
    python manage.py startapp music
    cd ..
}

Write-Host "Setup completed successfully."
