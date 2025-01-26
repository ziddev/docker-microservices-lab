from fastapi import FastAPI
from handlers import router as authentication_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the authentication router which contains routes for interacting with the authentications
app.include_router(authentication_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Authentication API is running!"}
