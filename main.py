from fastapi import FastAPI

app = FastAPI(title="Real-Time Food Delivery API")


@app.get("/")
def home():
    return {"message": "Food Delivery API is running", "status": "healthy"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
