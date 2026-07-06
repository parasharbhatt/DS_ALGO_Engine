from google import genai
from google.genai import types
from app.selection import SelectionSchema

def run_web_developer_agent(spec: SelectionSchema) -> str:
    client = genai.Client()
    
    prompt = f"""
    You are the Web_Developer_Agent. Build a professional, single-file HTML educational application.
    Target Specification:
    - Data Structure: {spec.data_structure}
    - Algorithm: {spec.algorithm}
    - Operations to Showcase: {', '.join(spec.operations)}
    - Code Language: {spec.language}

    CRITICAL INSTRUCTIONS:
    1. Output raw HTML code ONLY. Do NOT wrap your answer in markdown code blocks like ```html ... ```.
    2. Inside the file, include embedded CSS styles (<style>) and semantic elements.
    3. Include pure CSS variables and animations to visualize data states (e.g. keyframes for sorting/searching steps).
    4. Provide native inline SVG elements representing a clear step-by-step flowchart.
    5. Include interactive Vanilla Javascript (<script>) to step through logic, change states, and control animations.
    6. Include a dedicated code preview panel showing full implementation in {spec.language}.
    7. Include a visual algorithmic comparison chart (Big-O analysis for Time and Space complexities).
    8. Do NOT link external dependencies (No Bootstrap, no Tailwind, no external CDNs).
    """

    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2
        )
    )
    return response.text
