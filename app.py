from concurrent.futures import thread
from flask import Flask, render_template, request, redirect, flash, url_for
from waitress import serve
from models import db, User, Course
from covid import covid_obj
import random

from werkzeug.security import generate_password_hash

from flask_login import LoginManager, login_required, login_user, logout_user , current_user

from form import LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Hard coded secret key for development only
app.config['SECRET_KEY'] = "your-secret-key-here"
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# @app.route('/')
# def home() :
#     """Retrieve all users from the database"""
    
#     people = User.query.all()
    
#     return render_template("home.html", people=people)

# @app.route('/post-details/<int:id>')
# def post_details(id):
#     """Retrieve only one user(by id)"""
    
#     person = User.query.get(id)
    
#     return render_template("post-details.html", person=person)

# Only test
@app.route('/test')
def home_test():

    name = "INK WARUNTORN"
    return render_template("home_test.html", name=name)

# @app.route('/create')
# def create():
#     db.create_all()
#     return 'All tables created!'


@app.route('/about')
@login_required # New
def about():
    
    return render_template("about.html")


@app.route('/hi')
def index():
    return "Hello, with waitress!!!"


@app.route('/script')
def test_script():
    return render_template("test-script.html")

@app.route('/covid-table')
def covid_table():
    """Return covid19 data to show in a table"""
    
    covid_data = covid_obj
    return render_template("covid-table.html", covid_data=covid_data)

@app.route('/covid-dashboard')
def covid_dashboard() :
    """Return Covid19 data to display in a dashboard"""
    
    data = covid_obj
    new_case = data[0]["new_case"]
    total_case = data[0]["total_case"]
    new_case_excludeabroad = data[0]["new_case_excludeabroad"]
    total_case_excludeabroad = data[0]["total_case_excludeabroad"]
    new_recovered = data[0]["new_recovered"]
    total_recovered = data[0]["total_recovered"]
    new_death = data[0]["new_death"]
    total_death = data[0]["total_death"]
    case_prison = data[0]["case_prison"]
    case_walkin = data[0]["case_walkin"]
    update_date = data[0]["update_date"]
    
    
    
    return render_template("covid-dashboard.html",  new_case=new_case ,
                                                    total_case=total_case,
                                                    new_case_excludeabroad=new_case_excludeabroad,
                                                    total_case_excludeabroad=total_case_excludeabroad,
                                                    new_recovered=new_recovered,
                                                    total_recovered=total_recovered,
                                                    new_death=new_death,
                                                    total_death=total_death,
                                                    case_prison=case_prison,
                                                    case_walkin=case_walkin,
                                                    update_date= update_date
                            )
@app.route('/random-menu')
def random_menu():
    random_list = ["แกงผักหวานไข่มดแดง", "แกงอ่อม", "แกงหน่อไม้", "ต้มส้มปลานิล", "แกงเห็ด", "ต้มแซ่บกระดูกอ่อน"]
    menu_data = random.choice(random_list)
    
    return render_template('random-menu.html', menu_data=menu_data)


@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    """Create a new course"""
    # Check if method that being sent is "POST"
    if request.method == "POST" :
        
        # Create variables to get input attributes from form
        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]
        
        # Create an object, then pass variables into the class(Course)
        obj = Course(title=title,
                    instructor=instructor,
                    price=price,
                    duration=duration,
                    description=description)
        # Add the objects to SQLAlchemy session
        # then submit them into our database
        db.session.add(obj)
        db.session.commit()
        
        # Redirect to home page after submitting form
        return redirect(url_for('home'))
        
    return render_template('create-course.html')

@app.route('/')
def home() :
    """Retrieve all courses from the database"""
    
    all_courses = Course.query.all()
    
    return render_template("home.html", all_courses=all_courses)

@app.route('/post-details/<int:id>')
def post_details(id):
    """Retrieve only one course(by id)"""
    
    single_course = Course.query.get(id)
    
    return render_template("post-details.html", single_course=single_course)

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    """Update an existing post"""
    
    data = Course.query.get(id)
    
    # Check if method that being sent is "POST"
    if request.method == "POST" :
        
        # Create variables to get input attributes from form
        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]

        data.title = title
        data.instructor = instructor
        data.price = price
        data.duration = duration
        data.description = description
        
        # Submit an updated post into the database
        db.session.commit()
        
        # Redirect to home page after finishing update
        return redirect(url_for('home'))
    
    return render_template("update.html", data=data)

@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    """Delete a post"""
    
    data = Course.query.get(id)
    
    db.session.delete(data)
    db.session.commit()
    
    return redirect(url_for('home'))

@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    """Sign up user account"""
    
    # Check if method that being sent is "POST"
    if request.method == "POST":
        
        # Create variables to get input attribute values from our form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        
        # Create an object, then pass variables
        # into the User class
        obj = User(username=username,
                    password=generate_password_hash(password, method='sha256'),
                    email=email)
        
        # Add an object to SQLAlchemy session
        # then submit into our database
        db.session.add(obj)
        db.session.commit()
        
        # Redirect to home page after submitting form
        return redirect(url_for('home'))
    
    return render_template('sign-up.html')

# @app.route('/login') # Default is "GET" method
@app.route('/login', methods=['GET','POST']) # New --> add "POST"
def login():
    
    # Create an object called "form" to use LoginForm class
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    
    # Validate a form submitted by a user
    if form.validate_on_submit():
        
        # Query a user's username from the database
        user = User.query.filter_by(username=username).first()
        # Check and compare a user's password
        # in a database, if True, log a user in
        
        if user and user.verify_password(password):
            # Log a user in after completing verifying a password
            # then flash a message "Successful Login"
            login_user(user)
            flash("Successful Login", "success")
            # Redirect to homepage
            return redirect(url_for('home'))
        else:
            # Show flash message "Invalid Login" if login gets False
            flash("Invalid Login", "danger")
            
    else:
    # You can print or return something such as an error message
    # In this case, do nothing. But you can do it later
        pass
    return render_template('login.html', form=form)

# Create function by load_user for loading id from user
@login_manager.user_loader
def load_user(user_id) :
    
    return User.query.get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

mode = "dev" # developer mode
#mode = "prod"
if __name__ == "__main__":
    if mode == "dev":
        # app.run(debug=True)
        app.run(host='127.0.0.1', port=5000, debug=True)
    else:
        # Mode:Production
        serve(app, host='127.0.0.1', port=8080,
            threads=1)
