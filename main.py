from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Calculation(BaseModel):
    operation: str
    number1: float
    number2: float

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Calculator</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .calculator {{
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            input[type="number"], select {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
            }}
            button {{
                padding: 10px 15px;
                background-color: #007bff;
                border: none;
                color: white;
                border-radius: 5px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="calculator">
            <h2>FastAPI Calculator</h2>
            <form id="calcForm" action="/calculate/" method="post">
                <input type="number" name="number1" placeholder="Number 1" required>
                <input type="number" name="number2" placeholder="Number 2" required>
                <select name="operation" required>
                    <option value="">Select Operation</option>
                    <option value="add">Add</option>
                    <option value="subtract">Subtract</option>
                    <option value="multiply">Multiply</option>
                    <option value="divide">Divide</option>
                </select>
                <button type="submit">Calculate</button>
            </form>
            <div id="result"></div>
        </div>
    </body>
    </html>
    """)

@app.get("/hello")
async def hello_world():
    return {"message": "Hello World"}

@app.post("/calculate/")
async def calculate(
    operation: str = Form(...),
    number1: float = Form(...),
    number2: float = Form(...)
):
    if operation == "add":
        result = number1 + number2
    elif operation == "subtract":
        result = number1 - number2
    elif operation == "multiply":
        result = number1 * number2
    elif operation == "divide":
        if number2 == 0:
            return {"error": "Cannot divide by zero"}
        result = number1 / number2
    else:
        return {"error": "Invalid operation"}
    
    return {"result": result}
