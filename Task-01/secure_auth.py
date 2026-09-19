import json, os, hashlib, getpass
from datetime import datetime

FILE = "users.json"
session = None

def hash_pass(pwd):
    # prod grade: use bcrypt, here using sha256+salt for simplicity
    return hashlib.sha256((pwd + "PRODIGY_SALT").encode()).hexdigest()

def load():
    return json.load(open(FILE)) if os.path.exists(FILE) and open(FILE).read() else {}

def save(data):
    json.dump(data, open(FILE, 'w'), indent=4)

def register():
    u = input("New Username: ")
    users = load()
    if u in users: print("Already exists"); return
    p = getpass.getpass("New Password: ")
    role = input("Role user/admin [user]: ") or "user"
    users[u] = {"pwd": hash_pass(p), "role": role, "date": str(datetime.now())}
    save(users)
    print("Registered Successfully!")

def login():
    global session
    u = input("Username: ")
    p = getpass.getpass("Password: ")
    users = load()
    if u in users and users[u]["pwd"] == hash_pass(p):
        session = {"user": u, "role": users[u]["role"]}
        print(f"Welcome {u}! Login Successful")
        return True
    print("Login Failed!")
    return False

def protected():
    if not session:
        print("ACCESS DENIED! Login first.")
        return
    print(f"--- SECURE PAGE --- \nHello {session['user']} ({session['role']})")
    if session['role'] == 'admin':
        print("Admin View - All Users:", list(load().keys()))
    else:
        print("User View - You have limited access.")

while True:
    print("\n1.Register 2.Login 3.Protected Route 4.Logout 5.Exit")
    c = input("Choice: ")
    if c=='1': register()
    elif c=='2': login()
    elif c=='3': protected()
    elif c=='4': session=None; print("Logged out")
    elif c=='5': break
