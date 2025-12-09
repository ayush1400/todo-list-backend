from pymongo import MongoClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env file
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

# URL encode credentials to handle special characters
username = quote_plus(username)
password = quote_plus(password)

# MongoDB Atlas connection URI
uri = f"mongodb+srv://{username}:{password}@cluster0.2g49yfr.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.server_info()
    print("✅ Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("❌ Connection failed:", e)
    exit(1)

# Database & Collections
db = client["db_todo"]
todo_Table = db["db2_todo"]  # Todos collection
users = db["db3_login"]       # Users collection

# IMPORTANT: Create indexes with the CORRECT field names that match your app.py
try:
    # Drop the old incorrect index if it exists
    try:
        users.drop_index("email_1")
        print("🗑️  Dropped old 'email' index")
    except Exception:
        pass  # Index might not exist
    
    # Create unique index on email1 (matching your app.py field name)
    users.create_index("email1", unique=True)
    print("📧 Created unique index on 'email1' field")
    
    # Index on userId for faster todo queries
    todo_Table.create_index("userId")
    print("🔗 Created index on todo userId field")
except Exception as e:
    print("⚠️  Index creation warning:", e)

print(f"📊 Database: {db.name}")
print(f"👥 Users collection: {users.name}")
print(f"📝 Todos collection: {todo_Table.name}")