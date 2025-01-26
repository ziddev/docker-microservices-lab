from fastapi import FastAPI
from handlers import router as user_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the user router which contains routes for interacting with the users
app.include_router(user_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "User API is running!"}
