from fastapi import FastAPI
from handlers import router as article_router


# Create an instance of the FastAPI application to handle incoming requests
app = FastAPI()


# Include the article router which contains routes for interacting with the articles
app.include_router(article_router)


# Root endpoint to check if the API is running
@app.get("/")
async def root():
    return {"message": "Article API is running!"}
