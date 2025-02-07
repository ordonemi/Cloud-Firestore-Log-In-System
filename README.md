# Overview
This is a log in and authentication program that uses a Cloud Database to host the different accounts that can be created with this program and their respective information, such as username and passwords. At the start of the program, the user is presented with three options: Log into an account, create an account, and reset your password. In every option, the program will need to query the database to either create a new document, update a document's fields, or just pull fields from a document. 

Databases are the cornerstone of many software applications, and while developing this project my main goal was to gain a better understanding of how to correctly implement the use of a cloud database within a program. As I move further in my career it is more than likely that I will find myself developing software that need one or more databases. Naturally, one project will not be sufficient to gain a proficient knowledge, but rather this was meant to begin to build the foundations for further research and projects regarding this topic.

[Demonstration Video](https://youtu.be/e80wnHiVIMs)

# Cloud Database

Google Cloud Firestore

The database that was used for this program consists of an 'accounts' collection. Within that collection, each document corresponds to an account that was created using the program. Each document's unique ID is the email that was used to create an account. Each document has fields for a 'username' and 'password'.

# Development Environment
- Visual Studio Code
- Python 3.11.0
- Git/Github
- Google Cloud Firestore
- firebase_admin library
- markpass library 

# Useful Websites
- [Google Firebase Documentation](https://firebase.google.com/docs/firestore)
- [NoSQL on the Cloud With Python](https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc)

# Future Work
- After user logs in, display their statistics* 
- Determine what statistics to be saved
- Create a collection for statistics in the same databse
