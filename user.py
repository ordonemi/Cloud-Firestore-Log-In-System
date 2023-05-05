
import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firestore():
    """Create connection to database and document 'accounts'."""
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'userCredentials.json'
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'user-database-d29cb',
    })

    database = firestore.client()
    collection = database.collection('accounts')
    return collection


def create_account(collection):
    """Prompt the user for a new account to add to the database. The user will
       add a new username and password for the account they create."""

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

def log_in(collection):
    """Prompt the user to enter their username and password. Check if the username and password the user entered
       matches what is in the database."""
    
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

def reset_password(collection):
    """Prompt the user for the email they used to sign up,
       and change the password that is stored in the database under that email"""
    
    print('To reset your password, we need the email you used to create an account. If you don\'t have that, then we will need to create a new account.')
    have_email = input('\nDo you remember the email you used to create your account (y/n) ? ')
    check = True
    while (check):
        if (have_email == 'y'):
            email = input('\nEmail: ')
            doc = collection.document(email)
            res = doc.get().to_dict()

            print('Your username is: ' + res['username'])

            print('\nPlease enter the new password you would like to set below:')
            new_password = input('Password: ')
            pass_check = input('Enter the same password again: ')

            while(new_password != pass_check):
                print('\nPasswords do not match, please try again.')
                pass_check = input('Enter the same password again: ')
            
            doc.update({'password': new_password})

            print('\nPassword updated successfully!')
            return
  
        elif (have_email == 'n'):
            print('Please restart the program, and create a new account.\n')
            return
        else:
            print('Invalid input, please enter a \'y\' or \'n\'.')
            have_email = input('\nDo you remember the email you used to create your account (y/n) ? ')

def display_options():
    collection = initialize_firestore()
    print('\nWelcome to WTF!')
    print('Please select one of the options below:')
    print('     1.Log in to an existing account.')
    print('     2.Create a new account.')
    print('     3.Reset your password.\n')
    
    try:
        choice = int(input('Enter your choice: '))

        while (choice < 1 or choice > 3):
            print("Invalid choice selected. Please try again.")
            choice = int(input('Enter your choice: '))
        
        if (choice == 1):
            log_in(collection)
        elif (choice == 2):
            create_account(collection)
        else:
            reset_password(collection)
    except ValueError:
        print("Your choice must be an integer. Please restart.")

    os.system('cls')
    return choice

c = initialize_firestore()
reset_password(c)






