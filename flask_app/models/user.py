from flask_app.config.mysqlconnection import connectToMySQL 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import magazine
db = 'magazines'



class User:
    db = 'magazines'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines = []
    
    @classmethod
    def create_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for r in results:
            users.append(cls(r))
        return users

    @classmethod
    def show(cls,data):
        query= """
        SELECT * FROM magazines
        LEFT JOIN users ON magazines.user_id = users.id
        WHERE magazines.id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return results


    @classmethod
    def get_user_mag(cls,data):
        query = """SELECT * FROM magazines.users
        LEFT JOIN magazines ON magazines.user_id = users.id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        user = cls( results[0] )
        for r in results:
            mag_data = {
                'id': r['magazines.id'],
                'title': r['title'],
                'description': r['description'],
                'user_id': r['user_id'],
                'created_at': r['magazines.created_at'],
                'updated_at': r['magazines.updated_at']
            }
            user.magazines.append(magazine.Magazine(mag_data))
        return user



    @classmethod
    def by_id(cls,user_id):
        data={
            "id":user_id
        }
        query = """SELECT * FROM users 
        WHERE id = %(id)s;"""
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def by_email(cls, data):
        query = """SELECT * FROM users 
        WHERE email = %(email)s;"""
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def update(cls,data):
        query = """UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s,
        email=%(email)s
        WHERE id = %(id)s;"""
        result = connectToMySQL('magazines').query_db(query, data)
        return result

    @staticmethod
    def validate_user_reg(user):
        is_valid = True 
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results = connectToMySQL(User.db).query_db(query, user)

        if len(user['first_name']) < 3:
            flash("First name has to be greater than 2 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name has to be greater than 2 characters.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password has to be greater than 7 characters.", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.", "register")
            is_valid = False
        if len(results) >= 1:
            flash("Email is taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is invalid.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(user):
        is_valid = True 
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL(User.db).query_db(query, user)

        if len(user['first_name']) <= 3:
            flash("First name is required and must be at least 3 characters long.", "update")
            is_valid = False
        if len(user['last_name']) <= 3:
            flash("Last name is required and must be at least 3 characters long.", "update")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is invalid.", "update")
            is_valid = False
        return is_valid