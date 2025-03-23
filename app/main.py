from fastapi import FastAPI, WebSocket
import asyncio
import json
import random  # For simulating GPS data
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection (replace with your connection string)
client = MongoClient("mongodb://localhost:27017/")
db = client["tansatron"]
buses_collection = db["buses"]

# Store active WebSocket connections
connected_clients = set()

# Simulate GPS data for a bus (replace with actual GPS hardware integration later)
async def simulate_bus_location(bus_id: str):
    while True:
        latitude = 9.9312 + random.uniform(-0.05, 0.05)  # Simulated Kochi coordinates
        longitude = 76.2673 + random.uniform(-0.05, 0.05)
        location_data = {"bus_id": bus_id, "lat": latitude, "lng": longitude}
        
        # Store in MongoDB
        buses_collection.update_one({"bus_id": bus_id}, {"$set": location_data}, upsert=True)
        
        # Broadcast to all connected clients
        for client in connected_clients:
            await client.send_text(json.dumps(location_data))
        
        await asyncio.sleep(5)  # Update every 5 seconds

# WebSocket endpoint for live tracking
@app.websocket("/ws/live-tracking/{bus_id}")
async def websocket_endpoint(websocket: WebSocket, bus_id: str):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        # Start simulating location updates for this bus (in production, use real GPS data)
        asyncio.create_task(simulate_bus_location(bus_id))
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)

# REST endpoint to get initial bus data
@app.get("/bus/{bus_id}")
async def get_bus_data(bus_id: str):
    bus = buses_collection.find_one({"bus_id": bus_id})
    if bus:
        return {"bus_id": bus["bus_id"], "lat": bus["lat"], "lng": bus["lng"]}
    return {"error": "Bus not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)