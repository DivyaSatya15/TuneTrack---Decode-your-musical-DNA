
from database.db import get_connection
import bcrypt

# ========================================================================
# CONNECT TO DATABASE
# ========================================================================

connection = get_connection()
if connection: 
    cursor = connection.cursor()
    print("Database Connected Successfully!")
else:
    print("Failed to connect to the database.")
    exit()

# ========================================================================
# WELCOME SCREEN
# ========================================================================

print("========================================")
print("🎵 Welcome to TuneTrack")
print("Decode Your Musical DNA")
print("========================================")


# ========================================================================
# REGISTER USER
# =========================================================================

def register_user():
    print("\n========== Register ==========")

    username = input("Enter Username: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username, email, hashed_password))
        connection.commit()

        print("\n✅ Registration Successful!")

    except Exception as e:
        connection.rollback()
        print("\n❌ Registration Failed!")
        print(e)

# ========================================================================
# LOGIN USER
# ========================================================================

def login_user():
    print("\n==========Login==========")
    email = input("Enter Email:")
    password = input("Enter Password:")
    try:
        query = """
        SELECT username, password_hash
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            username = user[0]
            stored_password = user[1]

            if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
                print(f"\n🎉 Welcome back, {username}!")
            else:
                print("\n❌ Incorrect Password!")
        else:
            print("\n❌ Email not found.")
    except Exception as e:
        print(e)



# ========================================================================
# MAIN MENU
# ========================================================================


print("====================MAIN MENU====================")

print("\nChoose an option:")
print("1. Register")
print("2. Login")
print("3. Exit")

choice = input("\nEnter your choice:")
if choice == "1.":
    register_user()
elif choice == "2.":
    login_user()
elif choice == "3.":
    print("\nThank you for using TuneTrack!")
    connection.close()
else:
    print("\n Invalid choice.")