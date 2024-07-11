from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import os
import time
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    username: str
    password: str
    auth_option: str

@app.post("/start-selenium-task")
async def start_selenium_task(user_input: UserInput, background_tasks: BackgroundTasks):
    global processing_complete
    processing_complete = False

    with open('user_input.json', 'w') as f:
        json.dump(user_input.dict(), f)
    
    background_tasks.add_task(run_scripts, user_input.username, user_input.password, user_input.auth_option)
    return {"message": "User input received and scripts are running in the background"}

def run_scripts(username, password, auth_option):
    global processing_complete
    try:
        # Execute the Selenium script
        result = subprocess.run(['python3', 'ytLogging.py', username, password, auth_option], check=True)
        print(result)
        
        # Execute the API script
        result = subprocess.run(['python3', 'ytApi.py'], check=True)
        print(result)
        
        # Execute the data merging script
        result = subprocess.run(['python3', 'dataMerging.py'], check=True)
        print(result)

        processing_complete = True
    except subprocess.CalledProcessError as e:
        processing_complete = False
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/status")
def get_status():
    return {"processing_complete": processing_complete}


@app.get("/data")
def get_data():
    file_path = '../frontend/src/merged_data.json'  
    print(f"Checking for file at: {file_path}")
    if os.path.exists(file_path):
        print(f"File found: {file_path}")
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    else:
        print(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="Data not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
