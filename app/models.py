from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager




class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'urlandtinyurl'

    url = db.Column(db.String, primary_key=True)
    tiny_url = db.Column(db.String, primary_key=False)

    def __repr__(self):
        return f"Employee('{self.url}', '{self.tiny_url}')"


#class Department(db.Model):

#    Create a Department table


 #   __tablename__ = 'departments'

  #  id = db.Column(db.Integer, primary_key=True)