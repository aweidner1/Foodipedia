from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Recipes, FoodType, RecipeDirectory, RecipeManual, PersonalBook, Ingredient
from wtforms.fields.html5 import DateField
from datetime import datetime

#ssns = Department.query.with_entities(Department.mgr_ssn).distinct()


#Recipe Dropdown
rID =  Recipes.query.with_entities(Recipes.RecipeID).distinct()
fTypeID =  FoodType.query.with_entities(FoodType.FoodTypeID).distinct()
inID = Ingredient.query.with_entities(Ingredient.IngredientsID).distinct()

#rID = db.session.query(Recipes.RecipeID).distinct()

#FoodType Dropdown
cType = FoodType.query.with_entities(FoodType.CourseType).all()
#empSsnNames= Employee.query.with_entities(Employee.fname, Employee.lname, Employee.ssn).all()
#projNumNames= Project.query.with_entities(Project.pnumber, Project.pname).all()
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above

myChoices2 = [(row[0],row[0]) for row in fTypeID]  # change
results=list()
for row in fTypeID:
    rowDict=row._asdict()
    results.append(rowDict)
myChoices = [(row['FoodTypeID'],row['FoodTypeID']) for row in results]

results=list()
for row in inID:
    rowDict=row._asdict()
    results.append(rowDict)
myChoices3 = [(row['IngredientsID'],row['IngredientsID']) for row in results]

results=list()
for row in rID:
    rowDict=row._asdict()
    results.append(rowDict)
myChoices4 = [(row['RecipeID'],row['RecipeID']) for row in results]

# TESTING=list()
# for row in Recipes.query.all():
    # TESTING.append((Recipes.RecipeID, Recipes.FoodTypeID))
#results=list()


regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
regex=regex1 + regex2
class RegistrationForm(FlaskForm):
    Username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    confirm_Password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Sign Up')

    def validate_Username(self, Username):
        user = User.query.filter_by(Username=Username.data).first()
        if user:
            raise ValidationError('That Username is taken. Please choose a different one.')

    def validate_Email(self, Email):
        user = User.query.filter_by(Email=Email.data).first()
        if user:
            raise ValidationError('That Email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    Username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    Email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_Username(self, Username):
        if Username.data != current_user.Username:
            user = User.query.filter_by(Username=Username.data).first()
            if user:
                raise ValidationError('That Username is taken. Please choose a different one.')

    def validate_Email(self, Email):
        if Email.data != current_user.Email:
            user = User.query.filter_by(Email=Email.data).first()
            if user:
                raise ValidationError('That Email is taken. Please choose a different one.')


    
class RecipeUpdateForm(FlaskForm):


    RecipeID = HiddenField("")

    FoodName=StringField('Recipe Name:', validators=[DataRequired(),Length(max=15)])

    PrepTime = StringField('Prep Time')
    CookTime = StringField('Cook Time')
    Steps = StringField('Steps')
    #mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
    submit = SubmitField('Add Asssignment')



#Recipe Add Form
class AssignForm(FlaskForm):
 
    fTypeID = SelectField("Click on your FoodTypeID", coerce = int, choices=myChoices)
    steps = StringField("Instructions to cook")
    fName = StringField("FoodName")
    pTime = StringField("Prep Time")
    cTime = StringField("Cook Time")
   
    submit = SubmitField('Add Recipe')
    
    def validate_FID(self, FoodTypeID):    #because dnumber is primary key and should be unique
    #in parentheses before RecipeID: FoodTypeID=FoodTypeID.data,
        foodT = Recipes.query.filter_by(FoodTypeID=self.FoodTypeID.data).first()
        if recipe:
            raise ValidationError('That FoodTypeID number is taken. Please choose a different one.')


# got rid of def validate_dnumber

class AssignFormTwo(FlaskForm):
    #Instructions table 
    recipe = SelectField("Click on your Recipe ID", choices=myChoices4, coerce = int)
    ingred = SelectField("Click on the Ingredient ID", coerce = int, choices=myChoices3)
    measurements = StringField("Units of measurement", validators=[DataRequired(),Length(max=1000)])
    submit = SubmitField('Add Measurement')
    
    def validate_RecipeID(self, RecipeID):    #because dnumber is primary key and should be unique
        recipe = Recipes.query.filter_by(RecipeID=self.RecipeID.data).first()
        if recipe:
            raise ValidationError('That RecipeID number is taken. Please choose a different one.')

class RecipeForm(RecipeUpdateForm):

    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    submit = SubmitField('Add this department')

    def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
        dept = Department.query.filter_by(dnumber=dnumber.data).first()
        if dept:
            raise ValidationError('That department number is taken. Please choose a different one.')




