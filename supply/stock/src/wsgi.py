from fastapi import FastAPI
from handlers import router as stock_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the stock router which contains routes for interacting with the stocks
app.include_router(stock_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Stock API is running!"}
