from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")
    server_status = client.admin.command("serverStatus")
    print("MongoDB is running:", server_status)
except Exception as e:
    print("Failed to connect to MongoDB:", e)
