from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List

# Structural schema validation for Gemini output
class SelectionSchema(BaseModel):
    data_structure: str
    algorithm: str
    operations: List[str]
    language: str

def run_selection_agent(user_input: str) -> SelectionSchema:
    client = genai.Client()
    
    sys_instruction = (
        "You are the DS_Algo_PL_Selection_Agent. Process the user's intent. "
        "Extract the Data Structure, the target Algorithm, applicable operations, "
        "and the Programming Language choice (Python, Java, C, C++, or JavaScript). "
        "Strictly adhere to the structural output format."
    )
    
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruction,
            response_mime_type="application/json",
            response_schema=SelectionSchema,
            temperature=0.1 # Low temperature for accurate structure extraction
        )
    )
    return SelectionSchema.model_validate_json(response.text)
