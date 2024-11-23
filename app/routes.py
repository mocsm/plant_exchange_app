from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, Plant


# Home route
@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user:
            login_user(user)  # Log the user in
            return redirect(url_for('home'))
        else:
            return "User not found", 400  # Error if user doesn't exist

    return render_template('login.html')  # Render the login page


# Logout route
@app.route('/logout')
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('login'))  # Redirect to login page


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():  # Check if username already exists
            return "Username already exists", 400  # Error if username exists
        user = User(username=username)
        db.session.add(user)  # Add user to the database
        db.session.commit()
        login_user(user)  # Log the user in immediately after registration
        return redirect(url_for('home'))  # Redirect to the home page

    return render_template('register.html')  # Render the registration page


# View plants route
@app.route('/plants')
@login_required
def plants():
    all_plants = Plant.query.all()  # Get all plants
    return render_template('plants_list.html', plants=all_plants)


# Exchange plant route
@app.route('/exchange', methods=['GET', 'POST'])
@login_required
def exchange_plant():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']

        plant = Plant(name=name, description=description, image_url=image_url, user_id=current_user.id)
        db.session.add(plant)
        db.session.commit()
        return redirect(url_for('plants'))

    return render_template('exchange_plant.html')


# Plant details route
@app.route('/plant/<int:plant_id>')
@login_required
def plant_details(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    return render_template('plant_details.html', plant=plant)


# Confirmation after exchange route
@app.route('/confirm_exchange')
@login_required
def exchange_confirmation():
    return render_template('exchange_confirmation.html')
