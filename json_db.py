import json


# File path to the JSON database
DB_FILE_PATH = 'database.json'


def read_db():
    """Load the database from the JSON file."""
    with open(DB_FILE_PATH, 'r') as file:
        return json.load(file)


def change_db(db):
    """Save the database to the JSON file."""
    with open(DB_FILE_PATH, 'w') as file:
        json.dump(db, file, indent=4)


def add_user(username, email):
    """Add a new user to the database."""
    db = read_db()
    new_user = {
        "username": username,
        "email": email
    }
    db["users"].append(new_user)
    change_db(db)
    print(f"User {username} added successfully.")

def get_users():
    """Retrieve all users from the database."""
    db = read_db()
    return db["users"]

def delete_user(username):
    """Delete a user from the database by username."""
    db = read_db()
    db["users"] = [user for user in db["users"] if user["username"] != username]
    change_db(db)
    print(f"User {username} deleted successfully.")

# Example usage
if __name__ == "__main__":
    add_user("john_doe", "john@example.com")
    add_user("jane_doe", "jane@example.com")
    print("Users:", get_users())
    #delete_user("john_doe")
    print("Users after deletion:", get_users())
