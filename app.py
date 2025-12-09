# from flask import Flask, jsonify, request
# from flask_cors import CORS

# #from dotenv import load_dotenv
# import pymongo
# from config import todo_Table,users
# from bson import ObjectId

# # ────────────────── Your CRUD Functions (unchanged) ──────────────────
# app = Flask(__name__)
# CORS(app)

# def serialize(doc):
#     doc["_id"] = str(doc["_id"])
#     return doc

# @app.route("/create/<desc>/<completed>")
# def create_todo(desc,completed):
#     # desc = input("Enter text: ")
#     # completed = input("Done?: ")
#     todo_create = {"desc1": desc, "completed1": completed}
#     result = todo_Table.insert_one(todo_create)
#     print("Inserted User ID:", result.inserted_id)
#     return {
#         "_id": str(todo_create["_id"]),
#         "desc1": todo_create["desc1"],
#         "completed1": todo_create["completed1"]
#     }

# @app.route("/show")
# def show_todo():
#     todos = [serialize(u) for u in todo_Table.find()]
#     return jsonify({"todos": todos})
    
# @app.route("/update/<todo_id>", methods=["PUT"])
# def update_todo(todo_id):
#     try:
#         todo_id_obj = ObjectId(todo_id)
#     except:
#         return jsonify({"error": "Invalid ObjectId"}), 400

#     data = request.json  # data coming from frontend
#     update_fields = {}

#     if "desc1" in data:
#         update_fields["desc1"] = data["desc1"]

#     if "completed1" in data:
#         update_fields["completed1"] = data["completed1"]

#     if not update_fields:
#         return jsonify({"error": "No fields to update"}), 400

#     result = todo_Table.update_one({"_id": todo_id_obj}, {"$set": update_fields})

#     if result.modified_count == 1:
#         return jsonify({"message": "Todo updated"}), 200
#     else:
#         return jsonify({"error": "Todo not found"}), 404
    
# @app.route("/delete/<todo_id>")
# def todo_delete(todo_id):
#     try:
#         todo_id_obj = ObjectId(todo_id)
#     except:
#         return jsonify({"error": "Invalid ObjectId!"}), 400

#     result = todo_Table.delete_one({"_id": todo_id_obj})

#     if result.deleted_count == 1:
#         return jsonify({"message": "Todo deleted", "id": todo_id})
#     else:
#         return jsonify({"error": "Todo not found"}), 404

# # ────────────────── Your Authentication Functions (unchanged) ──────────────────

# @app.route("/signup/<username>/<email>/<pwd>")
# def signup(username,email,pwd):
#     signup_details = {"username1": username, "email1": email, "pwd1": pwd}
#     result = users.insert_one(signup_details)
#     print("Inserted User ID:", result.inserted_id)
#     return {
#         "_id": str(signup_details["_id"]),
#         "username1": signup_details["username1"],
#         "email1": signup_details["email1"],
#         "pwd1": signup_details["pwd1"]
#     }

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
    
#     email = data.get("email1")
#     pwd = data.get("pwd1")

#     # Find user by email
#     user = users.find_one({ "email1": email })
    
#     if not user:
#         return jsonify({"msg": "User not found"}), 404

#     # # Check password
#     # if not user["pwd1"] pwd:
#     #     return jsonify({"msg": "Incorrect password"}), 401

#     # Success login
#     return jsonify({
#         "msg": "Login successful",
#         "user": serialize(user)
#     }), 200

# # @app.route("/login")
# # def login():
# #     all_users = [serialize(u) for u in users.find()]
# #     return jsonify({"all_users": all_users })


 
# # ────────────────── Menu ──────────────────
# # def menu():
# #     while True:
# #         print("\n--- todo Management ---")
# #         print("1. Create todo ")
# #         print("2. Show All to-do list")
# #         print("3. Update todo")
# #         print("4. Delete todo ")
# #         print("5. Exit")
# #         choice = input("Enter choice: ")
# #         if choice == "1":  create_todo()
# #         elif choice == "2": show_todo()
# #         elif choice == "3": update_todo()
# #         elif choice == "4": todo_delete()
# #         elif choice == "5": break
# #         else: print("Invalid choice!")


# if __name__ == "__main__":
#     # menu()
#     app.run(debug=True,port=8000)
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
from config import todo_Table, users
from bson import ObjectId

app = Flask(__name__)
CORS(app)

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# ────────────────── Authentication Routes ──────────────────

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    pwd = data.get("password")
    
    # Check if user already exists
    existing_user = users.find_one({"email1": email})
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400
    
    signup_details = {
        "username1": username, 
        "email1": email, 
        "pwd1": pwd  # Using old field names to match existing DB
    }
    result = users.insert_one(signup_details)
    
    return jsonify({
        "message": "User created successfully",
        "userId": str(result.inserted_id),
        "username": username,
        "email": email
    }), 201

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     email = data.get("email")
#     pwd = data.get("password")

#     # Find user by email (using old field name)
#     user = users.find_one({"email1": email})
    
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     # Check password (using old field name)
#     if user.get("pwd1") != pwd:
#         return jsonify({"error": "Incorrect password"}), 401

#     # Successful login
#     return jsonify({
#         "message": "Login successful",
#         "user": {
#             "userId": str(user["_id"]),
#             "username": user.get("username1", ""),
#             "email": user.get("email1", "")
#         }
#     }), 200
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    pwd = data.get("password")

    # DEBUG: Print what we're searching for
    print(f"🔍 Searching for email: '{email}'")
    
    user = users.find_one({"email1": email})
    
    if not user:
        # DEBUG: Let's see what emails exist
        all_emails = [u.get("email1") for u in users.find()]
        print(f"❌ User not found. Existing emails: {all_emails}")
        return jsonify({"error": "User not found"}), 404

    # DEBUG: Check password
    stored_pwd = user.get("pwd1")
    print(f"🔐 Stored password length: {len(stored_pwd)}, Entered length: {len(pwd)}")
    print(f"🔐 Passwords match: {stored_pwd == pwd}")
    
    if stored_pwd != pwd:
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "userId": str(user["_id"]),
            "username": user.get("username1", ""),
            "email": user.get("email1", "")
        }
    }), 200
# ────────────────── Todo CRUD Routes (User-Specific) ──────────────────

@app.route("/todos/create", methods=["POST"])
def create_todo():
    """Create a todo for a specific user"""
    data = request.json
    user_id = data.get("userId")
    desc = data.get("description")
    
    if not user_id or not desc:
        return jsonify({"error": "userId and description are required"}), 400
    
    try:
        user_id_obj = ObjectId(user_id)
    except:
        return jsonify({"error": "Invalid userId"}), 400
    
    # Verify user exists
    user = users.find_one({"_id": user_id_obj})
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    todo_create = {
        "userId": str(user_id_obj),
        "desc1": desc,  # Using old field name
        "completed1": False  # Using old field name
    }
    result = todo_Table.insert_one(todo_create)
    
    return jsonify({
        "message": "Todo created successfully",
        "todo": {
            "_id": str(result.inserted_id),
            "userId": todo_create["userId"],
            "description": todo_create["desc1"],
            "completed": todo_create["completed1"]
        }
    }), 201

@app.route("/todos/<user_id>", methods=["GET"])
def get_user_todos(user_id):
    """Get all todos for a specific user"""
    try:
        user_id_obj = ObjectId(user_id)
    except:
        return jsonify({"error": "Invalid userId"}), 400
    
    # Verify user exists
    user = users.find_one({"_id": user_id_obj})
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Get all todos for this user
    todos_raw = todo_Table.find({"userId": user_id})
    todos = []
    for todo in todos_raw:
        todos.append({
            "_id": str(todo["_id"]),
            "userId": todo.get("userId", ""),
            "description": todo.get("desc1", ""),
            "completed": todo.get("completed1", False)
        })
    
    return jsonify({
        "userId": user_id,
        "username": user.get("username1", ""),
        "todos": todos
    }), 200

@app.route("/todos/update/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a specific todo"""
    try:
        todo_id_obj = ObjectId(todo_id)
    except:
        return jsonify({"error": "Invalid todo ID"}), 400

    data = request.json
    update_fields = {}

    # Map new field names to old field names
    if "description" in data:
        update_fields["desc1"] = data["description"]

    if "completed" in data:
        update_fields["completed1"] = data["completed"]

    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400

    result = todo_Table.update_one({"_id": todo_id_obj}, {"$set": update_fields})

    if result.modified_count == 1 or result.matched_count == 1:
        updated_todo = todo_Table.find_one({"_id": todo_id_obj})
        return jsonify({
            "message": "Todo updated successfully",
            "todo": {
                "_id": str(updated_todo["_id"]),
                "userId": updated_todo.get("userId", ""),
                "description": updated_todo.get("desc1", ""),
                "completed": updated_todo.get("completed1", False)
            }
        }), 200
    else:
        return jsonify({"error": "Todo not found"}), 404

@app.route("/todos/delete/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a specific todo"""
    try:
        todo_id_obj = ObjectId(todo_id)
    except:
        return jsonify({"error": "Invalid todo ID"}), 400

    result = todo_Table.delete_one({"_id": todo_id_obj})

    if result.deleted_count == 1:
        return jsonify({
            "message": "Todo deleted successfully",
            "deletedId": todo_id
        }), 200
    else:
        return jsonify({"error": "Todo not found"}), 404

@app.route("/todos/toggle/<todo_id>", methods=["PATCH"])
def toggle_todo(todo_id):
    """Toggle the completed status of a todo"""
    try:
        todo_id_obj = ObjectId(todo_id)
    except:
        return jsonify({"error": "Invalid todo ID"}), 400
    
    todo = todo_Table.find_one({"_id": todo_id_obj})
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    new_status = not todo.get("completed1", False)
    result = todo_Table.update_one(
        {"_id": todo_id_obj},
        {"$set": {"completed1": new_status}}
    )
    
    if result.modified_count == 1:
        updated_todo = todo_Table.find_one({"_id": todo_id_obj})
        return jsonify({
            "message": "Todo status toggled",
            "todo": {
                "_id": str(updated_todo["_id"]),
                "userId": updated_todo.get("userId", ""),
                "description": updated_todo.get("desc1", ""),
                "completed": updated_todo.get("completed1", False)
            }
        }), 200
    else:
        return jsonify({"error": "Failed to toggle todo"}), 400

# ────────────────── Admin/Debug Routes (Optional) ──────────────────

@app.route("/admin/all-todos", methods=["GET"])
def get_all_todos():
    """Get all todos from all users (for debugging)"""
    todos_raw = todo_Table.find()
    todos = []
    for todo in todos_raw:
        todos.append({
            "_id": str(todo["_id"]),
            "userId": todo.get("userId", ""),
            "description": todo.get("desc1", ""),
            "completed": todo.get("completed1", False)
        })
    return jsonify({"todos": todos}), 200

@app.route("/admin/all-users", methods=["GET"])
def get_all_users():
    """Get all users (for debugging)"""
    all_users_raw = users.find()
    all_users = []
    for user in all_users_raw:
        all_users.append({
            "_id": str(user["_id"]),
            "username": user.get("username1", ""),
            "email": user.get("email1", "")
            # Password removed for security
        })
    return jsonify({"users": all_users}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)