from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")

class Calculation(BaseModel):
    operation: str
    number1: float
    number2: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})

@app.post("/calculate/")
def calculate(calc: Calculation):
    if calc.operation == "add":
        result = calc.number1 + calc.number2
    elif calc.operation == "subtract":
        result = calc.number1 - calc.number2
    elif calc.operation == "multiply":
        result = calc.number1 * calc.number2
    elif calc.operation == "divide":
        if calc.number2 == 0:
            return {"error": "Cannot divide by zero"}
        result = calc.number1 / calc.number2
    else:
        return {"error": "Invalid operation"}
    
    return {"result": result}
