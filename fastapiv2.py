from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:3000",  # Adjust this to your React Native app's URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Atlas connection string (replace with your actual connection string)
client = MongoClient("mongodb+srv://<s.sandu2284@student.leedsbeckett.ac.uk>:<Porsche2002>@cluster0.mongodb.net/plant_database?retryWrites=true&w=majority")
db = client["plant_database"]
collection = db["sensor_data"]

class SensorData(BaseModel):
    temperature: float
    humidity: float

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.get("/sensor-data")
def get_sensor_data():
    latest_data = collection.find_one(sort=[("_id", -1)])
    if latest_data:
        return JSONResponse(
            content={
                "temperature": latest_data["temperature"],
                "humidity": latest_data["humidity"]
            }
        )
    return JSONResponse(
        content={"message": "No data found"},
        status_code=404
    )

@app.post("/store-sensor-data")
async def store_sensor_data(data: SensorData):
    try:
        # Insert data into MongoDB Atlas collection
        collection.insert_one(data.dict())
        print(f"Received sensor data: {data}")
        return {"message": "Data stored successfully"}
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/store-sensor-data")
def debug_sensor_data():
    return {"message": "Use POST to send sensor data"}
