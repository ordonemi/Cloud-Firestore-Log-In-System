
import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firestore():
    """Create connection to database."""
    
    cred = credentials.Certificate("userCredentials.json")
    firebase_admin.initialize_app(cred)
    database = firestore.client()
    return database

def create_account(db):
    """Prompt the user for a new account to add to the database. The user will
       add a new username and password for the account they create."""
    
    collection = db.collection('accounts')
    print('\nTo create a new account, you need a valid email, username, and password.')

    email = input('\nEnter a valid email: ')
    doc = collection.document(email)
    res = doc.get()
    while res.exists:
        print("This email is already associated with an account, please enter another email.")
        email = input('Enter a valid email: ')
        doc = collection.document(email)
        res = doc.get()

    username = input('Create an username: ')
    password = input('Choose a password: ')
    pass_check = input('Enter the same password again: ')

    while (password != pass_check):
        print('Both passwords must match, please try again.')
        pass_check = input('Enter the same password again: ')

    res = collection.document(email).set({
        'email': email,
        'password': pass_check,
        'username': username
    })
    print("\nAccount created!")

def log_in(db):
    """Prompt the user to enter their username and password. Check if the username and password the user entered
       matches what is in the database."""
    
    collection = db.collection('accounts')
    print('\nTo access your account, please provide the email you used to create your account.')
    email = input('\nEmail: ')

    doc = collection.document(email)
    res = doc.get()

    while (res.exists == False):
        print('No account is found associated with that email. Please try again.')
        email = input('Email: ')
        doc = collection.document(email)
        res = doc.get()

    res = res.to_dict()

    print('Now, please enter the username and password for your account.')
    username = input("Username: ")
    while (username != res['username']):
        print('Username is incorrect, please try again.')
        username = input('Username: ')
    
    password = input("Password: ")
    while (password != res['password']):
        print('Password is incorrect. Please try again.')
        password = input('Password: ')
    
    print('Login successful! Welcome back.')    

def display_options():
    db = initialize_firestore()
    print('\nWelcome to WTF!')
    print('Please select one of the options below:')
    print('     1.Log in to an existing account.')
    print('     2.Create a new account.')
    print('     3.Recover your account.\n')
    
    try:
        choice = int(input('Enter your choice: '))

        while (choice < 1 or choice > 3):
            print("Invalid choice selected. Please try again.")
            choice = int(input('Enter your choice: '))
        
        if (choice == 1):
            log_in(db)
        elif (choice == 2):
            create_account(db)
    except ValueError:
        print("Your choice must be an integer. Please restart.")

    os.system('cls')
    return choice


db = initialize_firestore()
log_in(db)







