from fastapi import FastAPI
from handlers import router as price_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the price router which contains routes for interacting with the prices
app.include_router(price_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Price API is running!"}
