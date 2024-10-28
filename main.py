from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging

# Initialize FastAPI
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up templates and static files
templates = Jinja2Templates(directory="templates")

# Pydantic model for calculation input
class Calculation(BaseModel):
    operation: str
    number1: float
    number2: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})

@app.post("/calculate/")
async def calculate(calc: Calculation):
    logging.info(f"Received calculation request: {calc}")
    
    if calc.operation == "add":
        result = calc.number1 + calc.number2
    elif calc.operation == "subtract":
        result = calc.number1 - calc.number2
    elif calc.operation == "multiply":
        result = calc.number1 * calc.number2
    elif calc.operation == "divide":
        if calc.number2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = calc.number1 / calc.number2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return {"result": result}

