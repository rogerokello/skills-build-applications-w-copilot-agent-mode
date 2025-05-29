from pymongo import MongoClient

def initialize_database():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")

    # Create or connect to the octofit_db database
    db = client["octofit_db"]

    # Check if collections already exist before creating them
    if "users" not in db.list_collection_names():
        db.create_collection("users")
    if "teams" not in db.list_collection_names():
        db.create_collection("teams")
    if "activity" not in db.list_collection_names():
        db.create_collection("activity")
    if "leaderboard" not in db.list_collection_names():
        db.create_collection("leaderboard")
    if "workouts" not in db.list_collection_names():
        db.create_collection("workouts")

    # Create unique index for the users collection
    db.users.create_index([("email", 1)], unique=True)

    # List collections
    collections = db.list_collection_names()
    print("Collections in octofit_db:", collections)

if __name__ == "__main__":
    initialize_database()
