# AI-Driven Data Structures & Algorithms Engine

An AI-assisted educational application that turns a natural-language data structures and algorithms goal into a self-contained interactive HTML application.

## Project Category

**Educational Technology / AI Developer Tool**

- Data structures and algorithms visualization
- Generative AI application
- Interactive web application generator
- Python backend with a serverless deployment option

## Features

- Converts prompts such as "Bubble Sort using an Array in Java" into an educational SPA.
- Uses Pydantic schemas to validate Gemini-generated metadata.
- Generates HTML with embedded CSS, vanilla JavaScript, SVG flowcharts, and Big-O analysis.
- Provides a local dashboard for generating and launching standalone applications.
- Includes unit tests and timestamped PDF test reports.
- Supports Docker and Google Cloud Run deployment.

## Tools and Technologies

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=000000)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)

Additional tools:

- Jinja2 templates
- Uvicorn
- python-dotenv
- ReportLab
- unittest
- Google Cloud Run and Google Cloud Artifact Registry

## Project Structure

```text
DS_Algo_Engine/
├── app/
│   ├── __init__.py
│   ├── selection.py       # Gemini planning agent and Pydantic schema
│   └── web_dev.py         # Gemini SPA generation agent
├── generated_spas/        # Generated standalone HTML applications
├── templates/
│   └── index.html         # FastAPI dashboard template
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py   # FastAPI pipeline tests
├── test_outputs/          # Timestamped PDF test reports
├── main.py                # FastAPI application and routes
├── run.py                 # Local Uvicorn server entry point
├── run_tests.py           # Test runner and PDF report generator
├── requirements.txt       # Python dependencies
├── Dockerfile             # Multi-stage container configuration
├── deploy_gcp.sh          # Google Cloud Linux deployment script
├── deploy_gcp.bat         # Google Cloud Windows deployment script
└── README.md
```

## Architecture

```text
User Prompt
    │
    ▼
Selection Agent ──► Validated Pydantic Specification
    │
    ▼
Web Developer Agent ──► Standalone HTML, CSS, JavaScript, and SVG
    │
    ▼
generated_spas/
```

The selection agent extracts the data structure, algorithm, operations, and target language. The web developer agent uses that specification to generate a standalone educational application.

## Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key
HOST=127.0.0.1
PORT=8000
PROJECT_ID=your_gcp_project_id
```

The API key and project settings must remain local and must not be committed to source control.

### 3. Run locally

```powershell
python run.py
```

Open `http://127.0.0.1:8000`.

## Usage

1. Enter a prompt describing the data structure, algorithm, operations, and implementation language.
2. Submit the prompt through the dashboard.
3. Review the validated specification returned by the selection agent.
4. Launch the generated standalone application.

Example prompt:

```text
Build a Bubble Sort app using an Array in Java with compare, swap, and step-through operations.
```

## Testing

Run the test suite and generate a PDF report:

```powershell
python run_tests.py
```

Reports are written to `test_outputs/`. Generated applications are written to `generated_spas/`.

## Docker

Build and run the application with Docker:

```powershell
docker build -t dsa-engine .
docker run --rm -p 8080:8080 --env-file .env dsa-engine
```

Open `http://localhost:8080`.

## Google Cloud Run

Set the required values in `.env`, then use the deployment script for your platform:

```powershell
.\deploy_gcp.bat
```

On Linux or macOS:

```bash
./deploy_gcp.sh
```
