#!/usr/bin/env python3
"""
OpenManus Web Server
FastAPI interface for running OpenManus as a web service
"""

import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from typing import Optional
import logging

# Import OpenManus components
from app.agent.manus import Manus
from app.config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OpenManus AI Agent", description="AI Agent Web Interface")

class TaskRequest(BaseModel):
    prompt: str
    max_steps: Optional[int] = 20

class TaskResponse(BaseModel):
    success: bool
    result: str
    error: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with task submission form"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenManus AI Agent</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
            textarea { width: 100%; height: 100px; padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #005a87; }
            .result { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; border-left: 4px solid #007cba; }
            .error { border-left-color: #d32f2f; background: #ffebee; }
            .loading { display: none; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 OpenManus AI Agent</h1>
            <p>Enter a task for the AI agent to perform:</p>
            
            <form id="taskForm">
                <textarea id="prompt" placeholder="Example: Search Google for latest AI news and summarize the top 3 articles" required></textarea>
                <br><br>
                <button type="submit">Execute Task</button>
                <div class="loading" id="loading">⏳ Processing your request...</div>
            </form>
            
            <div id="result" class="result" style="display:none;"></div>
        </div>
        
        <script>
        document.getElementById('taskForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const prompt = document.getElementById('prompt').value;
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            
            loading.style.display = 'block';
            result.style.display = 'none';
            
            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: prompt })
                });
                
                const data = await response.json();
                
                result.innerHTML = data.success 
                    ? `<h3>✅ Task Completed</h3><pre>${data.result}</pre>`
                    : `<h3>❌ Error</h3><pre>${data.error}</pre>`;
                result.className = data.success ? 'result' : 'result error';
                result.style.display = 'block';
                
            } catch (error) {
                result.innerHTML = `<h3>❌ Network Error</h3><pre>${error.message}</pre>`;
                result.className = 'result error';
                result.style.display = 'block';
            }
            
            loading.style.display = 'none';
        });
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """Execute an AI agent task"""
    try:
        logger.info(f"Executing task: {request.prompt}")
        
        # Initialize the agent
        agent = Manus()
        
        # Execute the task
        result = await agent.run(request.prompt, max_steps=request.max_steps)
        
        logger.info("Task completed successfully")
        return TaskResponse(success=True, result=str(result))
        
    except Exception as e:
        logger.error(f"Task execution failed: {str(e)}")
        return TaskResponse(success=False, result="", error=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "OpenManus AI Agent"}

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    try:
        # Check if config is loaded
        llm_config = config.llm
        
        return {
            "status": "online",
            "llm_model": llm_config.model if hasattr(llm_config, 'model') else "Not configured",
            "api_configured": bool(llm_config.api_key if hasattr(llm_config, 'api_key') else False)
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Get port from environment (for Railway, Render, etc.)
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"Starting OpenManus Web Server on port {port}")
    
    uvicorn.run(
        "web_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )