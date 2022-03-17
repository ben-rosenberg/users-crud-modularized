from flask_app.config.mysqlconnection import connectToMySQL


# Comments contain code review concerns/questions. Documentation is distinguished
# with triple single quote comments.
# General questions here:
# Naming? I know some names don't follow convention.
# Is there some way to manipulate the User instances directly for things like
# get_user and delete? I guess we never make instances until a query is run...
# Hmm. The purpose of the class is strictly for creating User instances for the
# rendered template after queries are made? What happens to those instances? Are
# they like, consumed in the controller?


DATABASE = 'users_db'

''' 
Class corresponding to the users table from the database. Dictionaries returned
by SQL queries are converted into User class instances which are then rendered
in the HTML templates by the controller.
'''
class User:
    def __init__(self, data: dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
    
    # Is it okay to separate all the vars like this?
    '''
    Get all users in table. Turns the list of dictionaries returned by the
    SELECT query into a list of instances of class User.
    URL: /users
    '''
    @classmethod
    def get_all(cls) -> list:
        query = 'SELECT * FROM users;'
        db = connectToMySQL(DATABASE)
        query_results = db.query_db(query)
        all_users = []
        for user in query_results:
            all_users.append(cls(user))
        return all_users
    
    # The data dictionary only contains the user id. Why can I not pass in the
    # ID directly?
    # How can I specify User instance return type? -> user?
    '''
    Get a single user from the users table. 
    URL: /users/<id>
    '''
    @classmethod
    def get_user(cls, data: dict):
        query = 'SELECT * FROM users \
            WHERE id = %(id)s;'
        db = connectToMySQL(DATABASE)
        query_results = db.query_db(query, data)
        this_user_instance = cls(query_results[0])
        return this_user_instance

    '''
    Create new user. Data contains first name, last name, and email, the rest
    is automated.
    URL: /users/create -> /users/<id>
    '''
    @classmethod
    def create(cls, data: dict) -> int:
        query = 'INSERT INTO users (first_name, last_name, email)\
            VALUES(%(first_name)s, %(last_name)s, %(email)s);'
        db = connectToMySQL(DATABASE)
        new_user_id = db.query_db(query, data)
        return new_user_id

    '''
    Update user at the appropriate ID.
    URL: users/<id>/update -> /users/<id>
    '''
    @classmethod
    def update_user(cls, data: dict) -> None:
        query = 'UPDATE users\
            SET first_name = %(first_name)s, \
            last_name = %(last_name)s, \
            email = %(email)s \
            WHERE id = %(id)s;'
        db = connectToMySQL(DATABASE)
        db.query_db(query, data)
        return None

    '''
    Delete user at the ID from the data dictionary.
    URL: /users/<id>/delete -> /users
    '''
    @classmethod
    def delete_user(cls, data: dict) -> None:
        query = 'DELETE FROM users WHERE id = %(id)s'
        db = connectToMySQL(DATABASE)
        db.query_db(query, data)
        return None