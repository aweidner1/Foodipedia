from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(20), unique=True, nullable=False)
    Password = db.Column(db.String(60), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.Username}')"



class RecipeDirectory(db.Model):
    __table__ = db.Model.metadata.tables['RecipeDirectory']
    
class Recipes(db.Model):
    __table__ = db.Model.metadata.tables['Recipes']

# used for query_factory
def getRecipes(columns=None):
    u = Recipes.query
    if columns:
        u = u.options(orm.load_only(*columns))
    return u

def getRecipesFactory(columns=None):
    return partial(getRecipes, columns=columns)

class FoodType(db.Model):
    __table__ = db.Model.metadata.tables['FoodType']
    
class RecipeManual(db.Model):
    __table__ = db.Model.metadata.tables['RecipeManual']
class PersonalBook(db.Model):
    __table__ = db.Model.metadata.tables['PersonalBook']
# class Instructions(db.Model):
    # __table__ = db.Model.metadata.tables['Instructions']
class Ingredient(db.Model):
    __table__ = db.Model.metadata.tables['Ingredient']

    

  
