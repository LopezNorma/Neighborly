from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask import flash

class Helpme:
    db = "neighborly"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    #CREATE NEW HELPME
    @classmethod
    def save_helpme(cls, data):
        query="""
            INSERT INTO helpmes (title, description, location, user_id)
            VALUES(%(title)s, %(description)s, %(location)s, %(user_id)s,);
        """

        return connectToMySQL(cls.db).query_db(query, data)
    
    #READ all HELPME
    @classmethod
    def get_all_helpmes(cls):
        query="""
            SELECT * FROM helpmes
            JOIN users ON helpmes.user_id = users.id;
        """

        results = connectToMySQL(cls.db).query_db(query)

        all_helpmes=[]

        for row in results:
            one_helpme = cls(row)

            user_data={
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_helpme.owner = user_model.User(user_data)
            all_helpmes.append(one_helpme)
        return all_helpmes
    
        #READ a single log of a single sighting from a single user
    @classmethod
    def get_one_helpme(cls, data):
        query="""
            SELECT * FROM helpmes
            JOIN users ON helpmes.user_id = users.id
            WHERE helpmes.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)

        one_helpme = cls(results[0])

        user_data={
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
        }
        one_helpme.owner = user_model.User(user_data)
        
        return one_helpme
    
    #UPDATE (edit a Helpme)
    @classmethod
    def update_helpme(cls, data):
        query="""
            UPDATE helpmes 
            VALUES(%(title)s, %(description)s, %(location)s, %(user_id)s,);
            WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)
    
    #DELETE A HELPME ENTRY
    @classmethod
    def delete_helpme(cls,data):
        query="""
            DELETE FROM helpmes
            WHERE id=%(id)s;
        """

    #VALIDATIONS FOR ENTERING A NEW HELPME
    @staticmethod
    def validate_helpme(data):
        is_valid=True

        if len(data['title']) ==0:
            flash("a Title must be entered", 'helpme')
            is_valid = False
        if len(data['description']) ==0:
            flash("Must enter a description!", 'helpme')
            is_valid = False
        if len(data['location']) ==0:
            is_valid = False
            flash("Must provide a location!", 'helpme')

        return is_valid




