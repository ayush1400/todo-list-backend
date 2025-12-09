from pymongo import MongoClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
username = quote_plus(username)
password = quote_plus(password)

uri = f"mongodb+srv://{username}:{password}@cluster0.2g49yfr.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    client.server_info()
    print("✅ Connected to MongoDB successfully!\n")
except Exception as e:
    print("❌ Connection failed:", e)
    exit(1)

db = client["db_todo"]
users = db["db3_login"]

print("=" * 60)
print("🔧 FIXING DATABASE")
print("=" * 60)

# Step 1: Drop the problematic index
print("\n1️⃣ Dropping old 'email' index...")
try:
    users.drop_index("email_1")
    print("   ✓ Dropped old 'email' index")
except Exception as e:
    print(f"   ℹ️  No old index to drop (this is fine): {e}")

# Step 2: Delete users with null email1 (broken records)
print("\n2️⃣ Cleaning up broken user records...")
result = users.delete_many({"email1": None})
print(f"   ✓ Deleted {result.deleted_count} broken user records")

# Step 3: Create correct index
print("\n3️⃣ Creating new index on 'email1'...")
try:
    users.create_index("email1", unique=True)
    print("   ✓ Created unique index on 'email1'")
except Exception as e:
    print(f"   ⚠️  Warning: {e}")

# Step 4: Show current valid users
print("\n4️⃣ Current valid users in database:")
valid_users = list(users.find())
if valid_users:
    for idx, user in enumerate(valid_users, 1):
        print(f"   {idx}. {user.get('username1')} ({user.get('email1')})")
else:
    print("   No users found - database is clean!")

print("\n" + "=" * 60)
print("✅ DATABASE FIXED!")
print("=" * 60)
print("\nYou can now:")
print("1. Sign up new users through the UI")
print("2. Login with existing users")
print("\nThe duplicate key error should be resolved.")