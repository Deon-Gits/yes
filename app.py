from fastapi import FastAPI, Query
import requests

app = FastAPI()

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d**len(digits) for d in digits) == n

def digit_sum(n):
    return sum(int(digit) for digit in str(n))

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    try:
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("even" if number % 2 == 0 else "odd")

        fun_fact_response = requests.get(f"http://numbersapi.com/{number}/math?json=true")
        fun_fact = fun_fact_response.json().get("text", "No fact available")

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": False,  # Perfect number check can be added
            "properties": properties,
            "digit_sum": digit_sum(number),
            "fun_fact": fun_fact
        }
    except Exception as e:
        return {"number": number, "error": True, "message": str(e)}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

