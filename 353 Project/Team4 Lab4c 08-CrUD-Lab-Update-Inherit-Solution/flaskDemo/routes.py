import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
#Change form imports
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecipeUpdateForm, RecipeForm, AssignForm, AssignFormTwo
#Change Model Imports
from flaskDemo.models import User, Recipes, FoodType, RecipeDirectory, RecipeManual, PersonalBook, Ingredient
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
#from flaskDemo import Matching


#Same Login Form
@app.route("/")
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.Password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('home')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
#Display recipes and attributes, Food name




@app.route("/home")
@login_required
def home():

    results = Recipes.query.join(RecipeManual,Recipes.RecipeID == RecipeManual.RecipeID) \
                .add_columns(Recipes.FoodName, Recipes.PrepTime, Recipes.CookTime, RecipeManual.UnitsOfMeasure) \
                .join(Ingredient, Ingredient.IngredientsID == RecipeManual.IngredientsID).add_columns(Ingredient.IngredientNames)

    return render_template('assign_home.html', title='Join', recipes=results)
   

#Same Registration Form

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = User(Username=form.Username.data, Email=form.Email.data, Password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




#Same as Previous
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#Same as Previous
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
           
        current_user.Username = form.Username.data
        current_user.Email = form.Email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.Username.data = current_user.Username
        form.Email.data = current_user.Email
    
    return render_template('account.html', title='Account', form=form)


                         

@app.route("/assign/new", methods=['GET', 'POST'])
@login_required
def new_assign():
    form = AssignForm()
    if form.validate_on_submit():
      #  assignment = Works_On(essn=form.ssn.data,pno=form.pnumber.data, hours=form.hours.data)
        #recipe = Recipes(RecipeOrigin=form.rOrigin.data, PrepTime=form.pTime.data, CookTime=form.cTime.data) FoodTypeID=form.fTypeID.data
       # foodTypeID = FoodType(FoodTypeID=form.fTypeID.data)
       # db.session.add(foodTypeID)
       # db.session.commit()
        
        food = Recipes(FoodTypeID=form.fTypeID.data,FoodName=form.fName.data,PrepTime=form.pTime.data,CookTime=form.cTime.data,Steps=form.steps.data,) #change 
        db.session.add(food)
        db.session.commit()
        
        # food = FoodType(FoodName=form.fName.data, CourseType=form.cType.data)
        # db.session.add(food)
        # db.session.commit()
        # # db.session.add(Matching(Recipes.RecipeID = Recipes.FoodTypeID))
        # # db.session.commit()
        # #IngredientsID=form.ingID.data,
        # ingredients = Ingredient(IngredientNames=form.ingredientName.data, IngredientType=form.ingredientTypes.data)
        # db.session.add(ingredients)
        # db.session.commit()
        # #RecipeID=form.rID.data,
        # recipes = Recipes(RecipeOrigin=form.rOrigin.data, PrepTime=form.pTime.data, CookTime=form.cTime.data)
        # db.session.add(recipes)
        # db.session.commit()
        # #RecipeManualID=form.rMID.data,
        # recipeManual = RecipeManual(UnitsOfMeasure=form.measurements.data)
        # db.session.add(recipeManual)
        
        # db.session.commit()
        # #InstructionID=form.insID.data,
        # # instructions = Instructions(Steps=form.steps.data)
        # # db.session.add(instructions)
        # db.session.commit()
        flash('You have added a new recipe!', 'success')
        return redirect(url_for('home'))
    return render_template('create_assign.html', title='New Recipe',
                           form=form, legend='New Recipe')
                           
@app.route("/measurements/new", methods=['GET', 'POST'])
@login_required
def new_assignTwo():
    form = AssignFormTwo()
    if form.validate_on_submit():
      #  assignment = Works_On(essn=form.ssn.data,pno=form.pnumber.data, hours=form.hours.data)
        #recipe = Recipes(RecipeOrigin=form.rOrigin.data, PrepTime=form.pTime.data, CookTime=form.cTime.data) FoodTypeID=form.fTypeID.data
        measurements = RecipeManual(RecipeID=form.recipe.data, IngredientsID=form.ingred.data, UnitsOfMeasure=form.measurements.data)
        db.session.add(measurements)
        db.session.commit()
        flash('You have added Measurements to your Ingredients!', 'success')
        return redirect(url_for('home'))
    return render_template('create_assignTwo.html', title='New Ingredient Specifications',
                           form=form, legend='New Ingredient Specifications')

#Already Changed
#@app.route("/assign/<IngredientsID>/<RecipeID>/<RecipeManualID>")
#@login_required
#def assign(IngredientsID, RecipeID, RecipeManualID):
#    assign = RecipeManual.query.get_or_404([IngredientsID,RecipeID,RecipeManualID])
#    return render_template('assign.html', title=str(assign.IngredientsID) + "_" + str(assign.RecipeID) + "_" + str(assign.RecipeManualID), assign=assign, now=datetime.utcnow())

@app.route("/assign/<RecipeID>/<IngredientsID>")
@login_required
def assign(RecipeID, IngredientsID):
    assign = RecipeManual.query.get_or_404([RecipeID,IngredientsID])
    return render_template('assign.html', title=str(assign.RecipeID) + "_" + str(assign.IngredientsID), assign=assign, now=datetime.utcnow())

#Need to Work on form and HTML pages
@app.route("/assign/<RecipeID>/<IngredientsID>delete", methods=['POST'])
@login_required
def delete_assign(RecipeID, IngredientsID):
    assign = RecipeManual.query.get_or_404([RecipeID,IngredientsID])
    db.session.delete(assign)
    db.session.commit()
    flash('The Recipe has been deleted', 'success')
    return redirect(url_for('home'))
    
@app.route("/assign/<RecipeID>/update", methods=['GET', 'POST'])
@login_required
def update_assign(RecipeID):
    recipe = Recipes.query.get_or_404(RecipeID)
    currentRecipe = recipe.FoodName

    #new FORM
    form = RecipeUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentRecipe !=form.FoodName.data:
            recipe.FoodName=form.FoodName.data
       
        recipe.PrepTime=form.PrepTime.data
        recipe.CookTime=form.CookTime.data
        recipe.Steps=form.Steps.data
        db.session.commit()
        flash('Your Recipe has been updated!', 'success')
        return redirect(url_for('home', RecipeID=RecipeID))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form
        #comes from FORM
        form.RecipeID.data = recipe.RecipeID
        form.FoodName.data = recipe.FoodName
       
        form.PrepTime.data = recipe.PrepTime
        form.CookTime.data = recipe.CookTime
        form.Steps.data = recipe.Steps
    return render_template('create_dept.html', title='Update Recipe',
                           form=form, legend='Update Recipe')


 #need to do update form and HTML pages
@app.route("/recipe/<RecipeID>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(RecipeID):
    recipe = Recipes.query.get_or_404(RecipeID)
    currentRecipe = recipe.FoodName

    #new FORM
    form = RecipeUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentRecipe !=form.FoodName.data:
            recipe.FoodName=form.FoodName.data
       
        recipe.PrepTime=form.PrepTime.data
        recipe.CookTime=form.CookTime.data
        recipe.Steps=form.Steps.data
        db.session.commit()
        flash('Your Recipe has been updated!', 'success')
        return redirect(url_for('home', RecipeID=RecipeID))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form
        #comes from FORM
        form.RecipeID.data = recipe.RecipeID
        form.FoodName.data = recipe.FoodName
        
        form.PrepTime.data = recipe.PrepTime
        form.CookTime.data = recipe.CookTime
        form.Steps.data = recipe.Steps
    return render_template('create_dept.html', title='Update Recipe',
                           form=form, legend='Update Recipe')







