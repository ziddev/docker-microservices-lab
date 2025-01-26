from fastapi import FastAPI
from handlers import router as review_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the review router which contains routes for interacting with the reviews
app.include_router(review_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Review API is running!"}
