from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Calculation(BaseModel):
    operation: str
    number1: float
    number2: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Calculator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .calculator {
                background: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            input[type="number"], select {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
            }
            button {
                padding: 10px 15px;
                background-color: #007bff;
                border: none;
                color: white;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
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

        <script>
            document.getElementById('calcForm').onsubmit = async function(event) {
                event.preventDefault();
                const formData = new FormData(this);
                const response = await fetch('/calculate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        operation: formData.get('operation'),
                        number1: parseFloat(formData.get('number1')),
                        number2: parseFloat(formData.get('number2'))
                    })
                });

                const result = await response.json();
                document.getElementById('result').innerText = 
                    result.error ? result.error : `Result: ${result.result}`;
            };
        </script>
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
    calc = Calculation(operation=operation, number1=number1, number2=number2)
    
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
