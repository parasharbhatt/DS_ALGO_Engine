@echo off
setlocal enabledelayedexpansion

:: ==========================================
:: PARSE CONFIGURATION VIA LOCAL .ENV FILE
:: ==========================================
set "ENV_FILE=.env"

if not exist "%ENV_FILE%" (
    echo ERROR: Local operational configuration asset '%ENV_FILE%' not found!
    echo Please create a .env file containing PROJECT_ID and GEMINI_API_KEY variables.
    exit /b 1
)

:: Parse and extract key configurations safely
for /f "tokens=1,2 delims==" %%A in (%ENV_FILE%) do (
    if "%%A"=="PROJECT_ID" set "PROJECT_ID=%%B"
    if "%%A"=="GEMINI_API_KEY" set "GEMINI_API_KEY=%%B"
)

if "%PROJECT_ID%"=="" (
    echo ERROR: Variable 'PROJECT_ID' is empty or missing inside your .env file.
    exit /b 1
)
if "%GEMINI_API_KEY%"=="" (
    echo ERROR: Variable 'GEMINI_API_KEY' is empty or missing inside your .env file.
    exit /b 1
)

set "SERVICE_NAME=dsa-orchestration-engine"
set "REPO_NAME=%SERVICE_NAME%-repo"
set "REGION=us-central1"

echo =====================================================
echo  Starting Cost-Effective Deployment to GCP Cloud Run 
echo =====================================================
echo Targeting GCP Project ID: %PROJECT_ID%

:: 1. Direct active terminal context to target project
call gcloud config set project %PROJECT_ID%

:: 2. Enable foundational serverless orchestration APIs 
echo Enabling necessary Cloud APIs...
call gcloud services enable ://googleapis.com ://googleapis.com ://googleapis.com

:: 3. Create a clean artifact management container repository if it doesn't exist
echo Setting up secure container engine repository...
call gcloud artifacts repositories create %REPO_NAME% --repository-format=docker --location=%REGION% --description="Docker repository for modern DSA App Engine" 2>nul

:: 4. Trigger cloud-native build compilation pipeline
echo Uploading and building source context via Cloud Build...
set "IMAGE_URI=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO_NAME%/%SERVICE_NAME%:latest"
call gcloud builds submit --tag %IMAGE_URI% .

:: 5. Deploy directly into zero-scaled Cloud Run instance
echo Deploying container directly to Google Cloud Run...
call gcloud run deploy %SERVICE_NAME% --image=%IMAGE_URI% --platform=managed --region=%REGION% --allow-unauthenticated --set-env-vars="GEMINI_API_KEY=%GEMINI_API_KEY%" --min-instances=0 --max-instances=2 --cpu=1 --memory=512Mi

:: ==========================================
:: AUTOMATED CACHE PRUNING & COST MITIGATION
:: ==========================================
echo.
echo =====================================================
echo  Running Automated Artifact Registry Cache Pruning   
echo =====================================================
set "IMAGE_PACKAGE=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO_NAME%/%SERVICE_NAME%"
echo Scanning for historical or untagged container builds in: %IMAGE_PACKAGE%

:: Loop and programmatically delete old container variants
for /f "tokens=*" %%D in ('gcloud artifacts docker images list %IMAGE_PACKAGE% --sort-by="CREATE_TIME" --format="value(DIGEST)" --filter="NOT tags=latest" 2^>nul') do (
    echo Deleting redundant build layer: %%D
    call gcloud artifacts docker images delete "%IMAGE_PACKAGE%@%%D" --quiet --delete-tags
)

echo =====================================================
echo  Deployment and Storage Pruning Successfully Complete!
echo =====================================================
pause
