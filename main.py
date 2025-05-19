from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from grading import grade_card

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/grade")
async def grade(file: UploadFile = File(...)):
    result = await grade_card(file)
    return result

@app.get("/")
def root():
    return {"message": "Raw2Rated Grading API is live!"}