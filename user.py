
import firebase_admin
from firebase_admin import credentials, firestore
import os
import maskpass


def initialize_firestore():
    """Create connection to database and document 'accounts'."""
    
    #Connect to firestore database using the credentials in the 'userCredenetials.json' file.
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'userCredentials.json'
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'user-database-d29cb',
    })

    database = firestore.client()

    #This program will only use the 'accounts' collection, so instead of returning the connected database I found it more
    #efficient to return the connected 'accounts' collection.
    collection = database.collection('accounts')
    return collection


def create_account(collection):
    """Prompt the user for a new account to add to the database. The user will
       add a new username and password for the account they create."""

    print('\nTo create a new account, you need a valid email, username, and password.')

    #Prompt the user for a valid email, in the Cloud Database the email serves as a document key.
    email = input('\nEnter a valid email: ')
    doc = collection.document(email)
    res = doc.get()

    #Check to see if an account already exists with the email provided, if so prompt for a different email address.
    while res.exists:
        print("This email is already associated with an account, please enter another email.")
        email = input('Enter a valid email: ')
        doc = collection.document(email)
        res = doc.get()

    #Each document has the fields 'username' and 'password', which need to be set when creating a new account. 
    username = input('Create an username: ')
    password = maskpass.askpass(prompt='Choose a password: ',mask='*')

    #Prompt for the password twice, as it's typically done by most services that let you create your own account.
    pass_check = maskpass.askpass(prompt='Enter the same password again: ',mask='*')

    #Both passwords must match, otherwise ask the user to enter the password again.
    while (password != pass_check):
        print('Both passwords must match, please try again.')
        pass_check = maskpass.askpass(prompt='Enter the same password again: ',mask='*')

    #Once the username and passwords have been set correctly, create a new document within the 'accounts' collection.
    res = collection.document(email).set({

        #Each document has the email that the user entered as its document ID, and has a field for email, password, username.
        'email': email,
        'password': pass_check,
        'username': username
    })

    #Notify the user that the account has been created successfully.
    print("\nAccount created!")

def log_in(collection):
    """Prompt the user to enter their username and password. Check if the username and password the user entered
       matches what is in the database."""
    
    #To begin the log in process, prompt the user for the email they used to create the account. 
    print('\nTo access your account, please provide the email you used to create your account.')
    email = input('\nEmail: ')

    #Use the user input for email as a document ID in the database.
    doc = collection.document(email)
    res = doc.get()

    #If no document is found what that ID, that means there is no 'account' under that email. Prompt the user for another email.
    while (res.exists == False):
        print('No account is found associated with that email. Please try again.')
        email = input('Email: ')
        doc = collection.document(email)
        res = doc.get()

    #Convert the document to a dictionary, so it's easy to access the username and password fields. 
    res = res.to_dict()

    #Once we have the connection to the document established, the user must enter the username and password that is saved in the document's fields.
    print('Now, please enter the username and password for your account.')
    username = input("Username: ")

    #Check if the username the user entered is the same as what is saved on the database.
    while (username != res['username']):
        print('Username is incorrect, please try again.')
        username = input('Username: ')
    
    password = maskpass.askpass(prompt="Password: ",mask='*')

    #Check if the password the user entered is the same as what is saved on the database.
    while (password != res['password']):
        print('Password is incorrect. Please try again.')
        password = maskpass.askpass(prompt='Password: ',mask='*')
    
    #Notify the user they have succesfully logged in. 
    print('Login successful! Welcome back.')
    return

def reset_password(collection):
    """Prompt the user for the email they used to sign up,
       and change the password that is stored in the database under that email"""
    
    #To be able to update a password field, the document key is needed. For this program, the email is needed.
    print('To reset your password, we need the email you used to create an account. If you don\'t have that, then we will need to create a new account.')
    have_email = input('\nDo you remember the email you used to create your account (y/n) ? ')
    check = True
    
    #If the user knows the email they used to create an account, they will be able to reset their password. IF not, they must restart the program
    #and create a new account.
    while (check):

        #The user knows the email they used.
        if (have_email == 'y'):

            #Prompt the user for the email, and connect to the corresponding document in the database.
            email = input('\nEmail: ')
            doc = collection.document(email)
            res = doc.get().to_dict()
            
            #For convenience, display the document's username field.
            print('Your username is: ' + res['username'])

            print('\nPlease enter the new password you would like to set below:')

            #Prompt the user for a new password. 
            new_password = maskpass.askpass(prompt='Password: ',mask='*')
            pass_check = maskpass.askpass(prompt='Enter the same password again: ',mask='*')

            #The password logic is the same as in the create_account() function, check that the password was entered twice.
            while(new_password != pass_check):
                print('\nPasswords do not match, please try again.')
                pass_check = maskpass.askpass(prompt='Enter the same password again: ',mask='*')
            
            #Update the password field in the document, effectively 'resetting' your password.
            doc.update({'password': new_password})

            #Notify the use their password was resetted successfully.
            print('\nPassword updated successfully!')
            return

        #The user does not know the email they used.
        elif (have_email == 'n'):
            print('Please restart the program, and create a new account.\n')
            return
        
        #Data validation. 
        else:
            print('Invalid input, please enter a \'y\' or \'n\'.')
            have_email = input('\nDo you remember the email you used to create your account (y/n) ? ')

def display_options():
    """Displays the menu of options for this program."""

    print('\nWelcome to What\'s That Fish!')
    print('Please select one of the options below:')
    print('     1.Log in to an existing account.')
    print('     2.Create a new account.')
    print('     3.Reset your password.\n')

def main():
    """Prompts the user to choose an option from the function above, and
       runs the respective function."""
    
    #Initialize connection to database collection 'accounts'.
    collection = initialize_firestore()
    
    try:
        run = True

        while (run):

            #Display menu.
            display_options()

            #Prompt the user to choose an option from the menu.
            choice = int(input('Enter your choice: '))

            #Data validation for user input.
            while (choice < 1 or choice > 3):
                print('Invalid choice selected. Please try again.')
                choice = int(input('Enter your choice: '))
        
            #User chooses to log into an account.
            if (choice == 1):
                os.system('cls')
                log_in(collection)

            #User chooses to create an account.
            elif (choice == 2):
                os.system('cls')
                create_account(collection)

            #User chooses to reset their password.
            else:
                os.system('cls')
                reset_password(collection)
        
            #Ask the user if they would like to run the program again.
            print('Would you like to do something else?')
            print('1. Yes')
            print('2. No')

            run_again = int(input('Enter your choice: '))

            while (run_again < 1 or run_again > 2):
                print('Invalid choice, please try again.')
                run_again = int(input('Enter your choice: '))

            if (run_again == 1):
                os.system('cls')
                run = True
            else:
                run = False
    
    #User does not enter an integer.
    except ValueError:
        print('Your choice must be an integer. Please restart.')
    os.system('cls')
    print('Goodbye!')

main()






