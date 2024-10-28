from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class Calculation(BaseModel):
    operation: str
    number1: float
    number2: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request, "result": None})

@app.post("/calculate/", response_class=HTMLResponse)
async def calculate(request: Request, number1: float = Form(...), number2: float = Form(...), operation: str = Form(...)):
    result = None
    error = None

    # Perform the calculation based on the operation
    if operation == "add":
        result = number1 + number2
    elif operation == "subtract":
        result = number1 - number2
    elif operation == "multiply":
        result = number1 * number2
    elif operation == "divide":
        if number2 == 0:
            error = "Cannot divide by zero"
        else:
            result = number1 / number2
    else:
        error = "Invalid operation"

    # Render the template with the result
    return templates.TemplateResponse("calculator.html", {"request": request, "result": result, "error": error})

@app.get("/hello")
async def hello_world():
    return {"message": "Hello World"}
