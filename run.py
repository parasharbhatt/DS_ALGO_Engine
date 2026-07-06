import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    
    # Fetch parameters with absolute fail-safe defaults
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    
    print(f"Initializing DSA System Server on http://{host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)

