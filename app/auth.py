"""Fake login: checks credentials against data.py, stores the current user and provides role checks -> employee, manager."""
from app.data import USERS

currentMember = None

def signIn(emailInput, passwordInput):
    global currentMember

    for user in USERS:
        if user["email"].strip().lower() == emailInput.strip().lower() and user["password"] == passwordInput:
            currentMember = user
            return currentMember
    return None

def signOut():
    global currentMember
    currentMember = None

def getCurrentMember():
    global currentMember
    return currentMember

