"""
LESSON 2: A small web API with FastAPI.

This is the Python version of an ASP.NET Core Minimal API.

Start the server:   uv run uvicorn app.main:app --reload
Then open:          http://127.0.0.1:8000/docs   (Swagger UI, built in)
Stop the server:    press Ctrl + C in the terminal
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Like:  var app = WebApplication.Create();
app = FastAPI(title="Survey API")


# ---------------------------------------------------------------
# MODELS (like C# DTO classes with [Required], [Range] attributes)
# Pydantic checks incoming JSON for you. Send rating=9 and it
# returns a 422 error automatically, like ModelState validation.
# ---------------------------------------------------------------
class SurveyIn(BaseModel):
    office: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)          # ge = greater or equal, le = less or equal
    comment: str = ""


class Survey(SurveyIn):                      # inherits all fields above, adds id
    id: int


# A plain list acts as our "database" for now (it resets when the server restarts).
surveys: list[Survey] = []
next_id = 1   

# ---------------------------------------------------------------
# ENDPOINTS
# C#:  app.MapGet("/surveys", () => surveys);
# ---------------------------------------------------------------
@app.get("/low-rated-surveys")
def list_low_rated_surveys() -> list[Survey]:
    return [survey for survey in surveys if survey.rating <= 2]

@app.get("/surveys")
def list_surveys() -> list[Survey]:
    return surveys

@app.delete("/surveys/{survey_id}")
def delete_survey(survey_id: int) -> Survey:
    for survey in surveys:
        if survey.id == survey_id:
            surveys.remove(survey)    # changes the SAME list (no "global" needed)
            return survey             # found it: stop here, returns 200
    raise HTTPException(status_code=404, detail="Survey not found")  # only reached if not found

@app.get("/surveys/{survey_id}")    
def get_survey(survey_id: int) -> Survey:
    for survey in surveys:
        if survey.id == survey_id:
            return survey
    raise HTTPException(status_code=404, detail="Survey not found")   # like return NotFound()


@app.post("/surveys", status_code=201)
def create_survey(data: SurveyIn) -> Survey:
    global next_id
    survey = Survey(id=next_id, **data.model_dump())
    next_id += 1
    surveys.append(survey)
    return survey


@app.get("/stats")
def stats() -> dict:
    if not surveys:                          # "not surveys" is True when the list is empty
        return {"count": 0, "average_rating": None}
    average = sum(s.rating for s in surveys) / len(surveys)
    return {"count": len(surveys), "average_rating": round(average, 2)}



@app.get("/")
def home() -> dict:
    return {"message": "Survey API is running. Go to /docs to try it."}
# ---------------------------------------------------------------
# YOUR TURN (exercises)
# 1. Add  DELETE /surveys/{survey_id}  that removes a survey (404 if missing).
# 2. Add  GET /surveys/low  that returns only surveys with rating <= 2.
#    (Put it ABOVE get_survey, or FastAPI will think "low" is an id.)
# 3. Write a test for each new endpoint in tests/test_main.py.
# ---------------------------------------------------------------
