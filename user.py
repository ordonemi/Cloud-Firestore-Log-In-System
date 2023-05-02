
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
    
    print('\nTo create a new account, you need a valid email, username, and password.')

    email = input('\nEnter a valid email: ')
    username = input('Create an username: ')
    password = input('Choose a password: ')
    pass_check = input('Enter the same password again: ')

    while (password != pass_check):
        print('Both passwords must match, please try again.')
        pass_check = input('Enter the same password again: ')

    collection = db.collection('accounts')
    res = collection.document(username).set({
        'email': email,
        'password': pass_check,
        'username': username
    })

def log_in(db):
    """Prompt the user to enter their username and password. Check if the username and password the user entered
       matches what is in the database."""
    
    print('\nPlease enter your credentials below.')
    username = input('\nUsername: ')
    
    database_username = get_username(db,username)

    while (database_username == None):
        choice = input('Would you like to try again? (y/n) ')

def get_username(db,username):
    collection = db.collection('accounts')
    doc = collection.document(username)

    res = doc.get()

    if res.exists:
        res = res.to_dict()
        return res['username']
    else:
        print('Username does not exist in database.')

def get_password(db,username):
    collection = db.collection('accounts')
    doc = collection.document(username)

    res = doc.get().to_dict()

    return res['password']

def display_options():
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
    except ValueError:
        print("Your choice must be an integer. Please restart.")

    os.system('cls')
    return choice


db = initialize_firestore()
log_in(db)







