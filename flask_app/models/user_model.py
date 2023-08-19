from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
#might need other imports like flash other classes and regex

db = 'neighborly'

class User:
    def __init__(self, data):
        self.id= data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        print('*****************')
        return cls(results[0])
    # this will help get user by email and if the result is empty it means didn't found a email

    @classmethod
    def det_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(db).query_db(query)
        users =[]
        for row in results:
            users.append(cls(row))
            return users
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        return results
    
    staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        print(user ['email'], '+++++++++++++++++++++++++++++++')  
        if len(results) >= 1:
            flash('email already token!!')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters long!!')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last_name must be at least 2 characters long!!')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email or password')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long!!')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Invalid email or password')
            is_valid = False
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        return is_valid
        
    classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(cls, data)
        print(results, "$$$$$$$$$$$")
        return cls(results[0])
