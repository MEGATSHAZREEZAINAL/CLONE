import os
import json
from functions_framework import https
import google.generativeai as genai
from pydantic import BaseModel
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskRequest(BaseModel):
    prompt: str
    max_steps: Optional[int] = 5

class TaskResponse(BaseModel):
    success: bool
    result: str
    error: Optional[str] = None

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
    logger.warning("GEMINI_API_KEY not found in environment variables")

def execute_simple_task(prompt: str) -> str:
    """
    Execute simple tasks using Gemini AI
    Note: This is a simplified version that doesn't include browser automation
    due to Firebase Cloud Functions limitations
    """
    try:
        if not model:
            return "Error: Gemini API key not configured"
        
        # Enhanced prompt for better responses
        enhanced_prompt = f"""
        You are OpenManus, an AI assistant that helps with various tasks. 
        
        User's request: {prompt}
        
        Please provide a helpful response. Note that this is running in a serverless environment 
        without browser automation capabilities, so:
        
        1. If the task involves web browsing or searching, provide guidance on how to do it manually
        2. If it involves data analysis, provide the analysis based on your knowledge
        3. If it involves programming, provide code examples
        4. Be helpful and informative in your response
        
        Respond in a clear, structured way.
        """
        
        response = model.generate_content(enhanced_prompt)
        return response.text
        
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")
        return f"Error: {str(e)}"

@https
def openmanus(request):
    """
    Firebase Cloud Function for OpenManus AI Agent
    """
    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    try:
        if request.method != 'POST':
            return (json.dumps({'error': 'Method not allowed'}), 405, headers)
        
        # Parse request
        request_json = request.get_json()
        if not request_json or 'prompt' not in request_json:
            return (json.dumps({'error': 'Missing prompt in request'}), 400, headers)
        
        task_request = TaskRequest(**request_json)
        
        logger.info(f"Processing task: {task_request.prompt}")
        
        # Execute the task
        result = execute_simple_task(task_request.prompt)
        
        # Add notice about limitations
        limitation_notice = "\n\n⚠️ Note: This is running on Firebase Cloud Functions with limited capabilities. For full browser automation features, consider deploying to Railway or Google Cloud Run."
        result_with_notice = result + limitation_notice
        
        response = TaskResponse(success=True, result=result_with_notice)
        
        return (json.dumps(response.dict()), 200, headers)
        
    except Exception as e:
        logger.error(f"Function execution failed: {str(e)}")
        error_response = TaskResponse(
            success=False, 
            result="", 
            error=f"Function execution failed: {str(e)}"
        )
        return (json.dumps(error_response.dict()), 500, headers)

# Health check endpoint
@https  
def health(request):
    """Health check endpoint"""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    health_status = {
        'status': 'healthy',
        'service': 'OpenManus AI Agent (Firebase)',
        'limitations': 'Browser automation not available in this environment',
        'api_configured': bool(GEMINI_API_KEY)
    }
    
    return (json.dumps(health_status), 200, headers)