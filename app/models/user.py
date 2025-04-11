# IMPORTS
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login

class User(UserMixin):
    # INIT: Initialize a User object
    def __init__(self, user_id, email, address, balance, firstname, lastname, password=None):
        self.uid = user_id 
        self.id = user_id 
        self.email = email
        self.address = address
        self.balance = balance
        self.firstname = firstname
        self.lastname = lastname
        self.password = password  

    # Authenticates user by email and password 
    @staticmethod
    def get_by_auth(email, password):
        # Select user who's email matches the email passed as a paramter
        rows = app.db.execute("""
        SELECT password, user_id, email, address, balance, firstname, lastname
        FROM Users
        WHERE email = :email
        """, email=email)

        # No such user exists
        if not rows:
            return None
        
        # Incorrect password
        stored_password = rows[0][0]
        if not check_password_hash(stored_password, password):
            return None
        
        # User authenticated, return user object
        else:
            return User(*rows[0][1:])

        
    # checks for existing account associated with an email
    @staticmethod
    def email_exists(email):
        rows = app.db.execute('''
        SELECT email
        FROM Users
        WHERE email = :email
        ''', email=email)
        return len(rows) > 0

    # ____________
    # METHOD
    # REGISTER: hashes password, insert data into User table 
    @staticmethod
    def register(email, password, address, balance, firstname, lastname):
        try:
            # insert the user and hash the password
            rows = app.db.execute('''
            INSERT INTO Users(email, password, address, balance, firstname, lastname)
            VALUES(:email, :password, :address, :balance, :firstname, :lastname)
            RETURNING user_id
            ''',
            email=email,
            password=generate_password_hash(password),
            address=address,
            balance=balance,
            firstname=firstname,
            lastname=lastname)

            # Set the uid based on the query return
            uid = rows[0][0]

            # Get the user details associated with that uid
            return User.get(uid)  
        
        # Error handling
        except Exception as e:
            app.logger.error(f"Error registering user: {e}")
            return None

    # Retrieve a user by their uid 
    @staticmethod
    @login.user_loader
    def get(uid):
        rows = app.db.execute('''
        SELECT user_id, email, address, balance, firstname, lastname
        FROM Users
        WHERE user_id = :uid''', uid=uid)
        return User(*(rows[0])) if rows else None
    
    # Update a field of a user object
    #TODO update query to not be susceptible
    @staticmethod
    def update_user(uid, field, value):
        # Method passes parameter directly after checking value for security
        valid_fields = ["password", "firstname", "lastname", "email", "address", "balance"]
        
        if field not in valid_fields:
            return {"error": f"Invalid field '{field}'. Valid fields are: {', '.join(valid_fields)}."}
        
        try:
            # Hash input password to add to database
            if field == "password":
                value = generate_password_hash(value)
            query = f'''
            UPDATE Users
            SET {field} = :value
            WHERE user_id = :uid
            RETURNING user_id, email, address, balance, firstname, lastname
            '''
            rows = app.db.execute(query, value=value, uid=uid)

            # Return the updated user object
            return User(*(rows[0])) if rows else None
        
        # Error handling
        except Exception as e:
            print(str(e))
            return None
