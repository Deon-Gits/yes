# app/main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .number_utils import (
    is_prime, 
    is_armstrong_number, 
    get_digit_sum, 
    get_fun_fact
)
import math

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/classify-number", response_class=JSONResponse)
async def classify_number(number: str = Query(..., min_length=1)):
    try:
        # Convert input to float first
        n = float(number)

        # Convert to integer if it is a whole number
        if n.is_integer():
            n = int(n)

        # Determine properties
        properties = []
        if isinstance(n, int):  # Only integers should be classified as even/odd or Armstrong
            properties.append("even" if n % 2 == 0 else "odd")

            # Only non-negative integers can be Armstrong numbers
            if n >= 0 and is_armstrong_number(n):
                properties.append("armstrong")

        # Construct response
        return JSONResponse(
            status_code=200,
            content={
                "number": n,
                "is_prime": is_prime(n) if isinstance(n, int) and n > 1 else False,  # Only check for primes if n > 1
                "is_perfect": False,  # Placeholder (you can add perfect number logic)
                "properties": properties,
                "digit_sum": get_digit_sum(abs(int(n))) if isinstance(n, int) else sum(int(d) for d in str(abs(n)) if d.isdigit()),
                "fun_fact": get_fun_fact(abs(int(n))) if isinstance(n, int) else "No specific fun fact for non-integer numbers"
            }
        )

    except ValueError:
        # Handle invalid input (non-numeric values)
        return JSONResponse(
            status_code=400,
            content={
                "number": number,
                "error": True,
                "message": "Invalid number format"
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    import math
import requests

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong_number(n):
    """Check if a number is an Armstrong number."""
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

def get_digit_sum(n):
    """Calculate the sum of digits."""
    return sum(int(digit) for digit in str(n))

def get_fun_fact(number):
    """Fetch a fun fact about the number from Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math")
        return response.text if response.status_code == 200 else "No fun fact available"
    except:
        return "No fun fact available"

