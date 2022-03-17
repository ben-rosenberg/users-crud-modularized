from flask_app.config.mysqlconnection import connectToMySQL


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