import re

def check_password_strength(password):
    score = 0
    feedback = []
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters")
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Use both uppercase and lowercase")
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add at least one number")
    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add at least one special character")
    
    if score == 4:
        print("Strength: STRONG")
    elif score == 3:
        print("Strength: MEDIUM")
    else:
        print("Strength: WEAK")
        
    for f in feedback:
        print(f"- {f}")

pwd = input("Enter password: ")
check_password_strength(pwd)
