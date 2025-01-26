from fastapi import FastAPI
from handlers import router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the authentication and product routers which contains routes for interacting with the backend
app.include_router(router)

# Root endpoint to check if the backend is running
@app.get("/")
async def root():
    return {"message": "Backend is running!"}
