from flask_app.config.mysqlconnections import connectToMySQL
import re	# the regex module   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.user_models import User

class Order:
    db = "banh_mi"
    def __init__(self,data):
        self.id = data['id']
        self.item = data['item']
        self.description = data['description']
        self.price = data['price']
        self.user_id = data['user_id']
        self.users = None

    @classmethod 
    def save (cls,data):
        query = "INSERT INTO orderss (title, description, user_id) VALUES (%(title)s, %(description)s,  %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_one_order(cls, data):
        query = "SELECT * FROM paintings WHERE id =%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls (result[0])
    
    @classmethod
    def get_all_orders(cls):
        query = "SELECT * FROM paintings"
        results = connectToMySQL(cls.db).query_db(query)
        magazines = []
        for row in results:
            magazines.append(cls(row))
        return results
    
    @staticmethod
    def validate_order(magazine):
        is_valid = True
        query = "SELECT * from magazines WHERE user_id = %(user_id)s"
        if len(magazine['title']) < 2:
            flash ("Title must be at least 2 characters long!")
            is_valid = False
        if len(magazine['description']) < 10:
            flash ("Description must be at least 10 characters long!")
            is_valid = False
        return is_valid

    @classmethod
    def get_order_by_id(cls, id):
        query = "SELECT * FROM magazines LEFT JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, id)
        magazine= cls(results[0])
        user_data = {
                'first_name': results[0]['first_name'],
                'last_name': results[0] ['last_name'],
                'id': results[0]['users.id'],
                'email': results[0]['email'],     ## dont need to be ['user.email or password cause these are unique']
                'password': results[0]['password'], 
                'created_at': results[0]['users.created_at'],
                'updated_at': results [0]['users.updated_at']    
            }
        magazine.user= User(user_data)
        return magazine
        
    @classmethod
    def delete_order(cls, id):
        query = """
        DELETE FROM orderss WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return results

    @classmethod 
    def get_everything(cls):
        query = "SELECT * FROM orders LEFT JOIN users on orders.user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        magazines = []
        for row in results: 
            order= cls(row)
            user_data = {
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'id': row['users.id'],
                'email': row['email'],     ## dont need to be ['user.email or password cause these are unique']
                'password': row['password'], 
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            order.users = User(user_data)
            magazines.append(order)
        return magazines
    
    @classmethod 
    def get_user_with_magazine (cls):
        query = "SELECT * FROM magazines JOIN users ON users.id = magazines.user_id;"
        return connectToMySQL(cls.db).query_db(query)