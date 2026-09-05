from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Calculator import Calculator


app = FastAPI(title="Calculator")
calc = Calculator()


class MathRequest(BaseModel):
    expression: str


@app.post("/calculate")
def calculate(req: MathRequest):
    try:
        result = calc.evaluate(req.expression)
        calc.add_to_history(result)

        return {
            "input": req.expression,
            "result": str(result)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/history")
def get_history():
    return {"history": [str(item) for item in calc.history]}