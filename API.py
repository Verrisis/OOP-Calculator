from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from Calculator import Calculator
from EmptyHistoryError import EmptyHistoryError

app = FastAPI(title="Calculator")
calc = Calculator()


class MathRequest(BaseModel):
    expression: str


@app.post("/calculate")
def calculate(req: MathRequest):
    expression = req.expression.strip()

    if not expression:
        raise HTTPException(status_code=400, detail="Expression cannot be empty")

    try:
        result = calc.evaluate(expression)
        calc.add_to_history(result)
        return {
            "input": expression,
            "result": str(result),
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Input error: {str(e)}")
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=f"Unsupported operator: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/history")
def get_history():
    try:
        if not calc.history:
            raise EmptyHistoryError("Operation history is empty")

        return {"history": [str(item) for item in calc.history]}

    except EmptyHistoryError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
