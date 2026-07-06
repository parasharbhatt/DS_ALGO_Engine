import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.selection import run_selection_agent
from app.web_dev import run_web_developer_agent

load_dotenv()

app = FastAPI(title="AI DSA Engine Developer Workspace")

#templates = Jinja2Templates(directory="templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Ensure output directory exists
os.makedirs("generated_spas", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # FIX: Explicitly pass request=request as a standalone keyword argument
    return templates.TemplateResponse(
        name="index.html", 
        context={"success": False},
        request=request
    )

@app.post("/generate")
async def generate_app(request: Request, prompt: str = Form(...)):
    # Step 1: Fire Selection Agent
    selection_specs = run_selection_agent(prompt)
    
    # Step 2: Pass structure to Web Developer Agent
    html_content = run_web_developer_agent(selection_specs)
    
    # Create web-safe filename
    safe_name = f"{selection_specs.data_structure}_{selection_specs.algorithm}".lower().replace(" ", "_")
    filepath = f"generated_spas/{safe_name}.html"
    
    # Step 3: Write standalone file to workspace
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    # FIX: Explicitly pass request=request as a standalone keyword argument
    return templates.TemplateResponse(
        name="index.html",
        context={
            "success": True,
            "filename": f"{safe_name}.html",
            "specs": selection_specs.model_dump()
        },
        request=request
    )



@app.get("/view/{filename}")
async def view_spa(filename: str):
    # 1. Define the safe root directory
    base_dir = os.path.abspath("generated_spas")
    
    # 2. Build the absolute path to the requested file
    file_path = os.path.abspath(os.path.join(base_dir, filename))
    
    # SECURITY GUARD: Prevent directory traversal exploits (e.g., passing "../../etc/passwd")
    if not file_path.startswith(base_dir):
        raise HTTPException(status_code=403, detail="Access denied: Invalid directory scope.")
    
    # 3. Check if the generated application actually exists on your hard drive
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="The requested application has not been generated yet.")
        
    # 4. Stream the single self-contained HTML application directly to the browser
    return FileResponse(file_path, media_type="text/html")
