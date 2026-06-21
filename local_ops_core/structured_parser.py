import json
import os
import ollama
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class LogAnalysis(BaseModel):
    has_error: bool = Field(description="True if the log entry contains an error")
    error_code: int = Field(description="The HTTP or system error code, otherwise 0")
    summary: str = Field(description="A short summary of the incident in one sentence")

def extract_structured_data(log_line: str) -> LogAnalysis:
    # Explicitly write down the field descriptions in the prompt so the SLM understands the context
    prompt = f"""Analyze the provided log entry and extract the required fields. 
    Fill out the JSON keys based on these exact rules:
    - 'has_error': Look for keywords like ERROR, CRITICAL, or FAIL. Set to true or false.
    - 'error_code': Extract the numeric HTTP status code (e.g., 500) or system error code. If none is found, use 0.
    - 'summary': Write a concise, one-sentence English summary explaining what happened.

    Log entry to analyze: {log_line}"""
    
    response = ollama.generate(
        model=os.getenv("OLLAMA_MODEL", "llama3.2:latest"),
        prompt=prompt,
        format=LogAnalysis.model_json_schema(), # guarantees the JSON keys match Pydantic perfectly
        options={"temperature": 0.0} 
    )
    
    return LogAnalysis.model_validate_json(response['response'])

if __name__ == "__main__":
    sample_log = "2026-05-31 21:40:01 - ERROR - [METRICS] - Connection failed with status 500"
    result = extract_structured_data(sample_log)
    print(result.model_dump_json(indent=2))