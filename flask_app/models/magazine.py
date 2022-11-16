from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
db = "magazines"



class Magazine:
    db = "magazines"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def add_magazine(cls, data):
        query = """INSERT INTO magazines (title, description, user_id)
        VALUES (%(title)s, %(description)s, %(user_id)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result


    @classmethod
    def get_one_magazine(cls, data):
        query = """
        SELECT * FROM magazines 
        WHERE id = %(id)s;
        """
        results = connectToMySQL('magazines').query_db(query, data)
        return cls(results[0])


    @classmethod
    def get_all_magazines(cls):
        query = """SELECT * FROM magazines;
        """
        results = connectToMySQL('magazines').query_db(query)
        all_magazines = []
        for magazine in results:
            all_magazines.append(cls(magazine))
        return all_magazines

    


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM magazines WHERE id= %(id)s;"
        return connectToMySQL('magazines').query_db(query,data)


    @staticmethod
    def validate_magazine(magazine):
        is_valid = True 
        query = """SELECT * FROM magazines WHERE user_id = %(user_id)s;"""
        results = connectToMySQL(Magazine.db).query_db(query, magazine)

        if len(magazine['title']) < 3:
            flash("Title is required and must be at least 3 characters long.", "report")
            is_valid = False
        if len(magazine['description']) < 1:
            flash("Description is required and must be at least 10 characters long.", "report")
            is_valid = False
        return is_valid