from fastapi import FASTAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agent import run_agent
import uvicorn

#initialize app and templates
app = FASTAPI()
templates = Jinja2Templates(directory="templates")


#Request model
class AgentRequest(BaseModel):
    """Request model for agent invocation"""
    prompt:str #request type



#Response model
class AgentResponse(BaseModel):
    """Response model for agent invocation"""
    response: str



#home route
@app.get('/')
async def home(request:Request):
    """Serve the main html page"""
    return templates.TemplateResponse("index.html", {"request": request})


#invoke the agent
@app.post("/agent", response_model= AgentResponse)
async def invoke_agent(request: AgentResponse):
    """
    Invoke the agent with a prompt.

    The agent can read and write to a text file 
    
    """
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        #run the agent with the user's prompt
        result = run_agent(request.prompt)

        return AgentResponse(response= result)
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error invoking agent: {str(err)}")


uvicorn.run(app, host="0.0.0.0", port=8000)