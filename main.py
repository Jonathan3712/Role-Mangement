# from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
# import mysql.connector
# import logging

from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
from flask_cors import CORS
import mysql.connector
import logging

# from logging.handlers import RotatingFileHandler
# from flask import render_template, request, redirect, url_for, flash\

app = Flask(__name__)
app.secret_key = "b'\x94\xdd\xac\x84\xb6\xedy\x8c\x91c\xf8\x168l\xe9\xb4|>\xc8\xc3\x15XH\x1a'"

# Allow Next.js dev server (localhost:3000) to call /api/* routes
# CORS(
#     app,
#     resources={r"/api/*": {"origins": "http://localhost:3000"}},
#     supports_credentials=True,
# )
CORS(app)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s in %(module)s: %(message)s')

# Log HTTP requests
@app.before_request
def log_request_info():
    app.logger.info('%s %s %s', request.method, request.url, request.headers)

# Log HTTP responses
@app.after_request
def log_response_info(response):
    app.logger.info('%s %s', response.status, response.headers)
    return response





# Connect to MySQL database
db = None
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin@3712",
        database="suny"
        )
    app.logger.info("Connected to MySQL database successfully.")
except mysql.connector.Error as e:
    app.logger.error(f"Error connecting to MySQL: {e}")





# Define routes
@app.route('/')
def home():
    # Log the event
    app.logger.info('User accessed the home page')
    return render_template('index.html')
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM LogIn_Credential WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            cursor.execute("INSERT INTO LogIn_Credential (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            db.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    # Log the event
    app.logger.info('User accessed the home page')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database to check if username and password match
        cursor = db.cursor()
        cursor.execute("SELECT * FROM LogIn_Credential WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # Authentication succeeded, set session variables
            session['username'] = user[1]
            session['role'] = user[3]  # Assuming the role is stored at index 3 in the user tuple
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    # Log the event
    app.logger.info('User accessed the home page')
    # Render the login page when the request method is not 'POST'
    return render_template('login.html')


def get_access_privileges_for_role(role: str):
    """
    Return a dictionary of table -> access based on user's role.
    This makes the logic reusable for both HTML and JSON responses.
    """
    # Default: no access
    privileges = {
        'SE_Data': 'No Access',
        'HR_Data': 'No Access',
        'PR_Data': 'No Access',
        'Emp_SE': 'No Access',
        'Emp_HR': 'No Access',
        'Emp_PR': 'No Access',
        'LogIn_Credential': 'No Access',
    }

    if role == 'Admin':
        for key in privileges.keys():
            privileges[key] = 'Read/Write'
    elif role == 'SE':
        privileges['SE_Data'] = 'Read/Write'
        privileges['Emp_SE'] = 'Read/Write'
    elif role == 'HR':
        privileges['HR_Data'] = 'Read/Write'
        privileges['Emp_HR'] = 'Read/Write'
        privileges['Emp_PR'] = 'Read/Write'
        privileges['Emp_SE'] = 'Read'
    elif role == 'PR':
        privileges['PR_Data'] = 'Read/Write'
        privileges['Emp_PR'] = 'Read/Write'
        privileges['Emp_SE'] = 'Read'
        privileges['Emp_HR'] = 'Read'
    elif role == 'General':
        privileges['Emp_SE'] = 'Read'
        privileges['Emp_HR'] = 'Read'
        privileges['Emp_PR'] = 'Read'

    return privileges





# @app.route('/dashboard')
# def dashboard():
#     if 'username' in session:
#         # Implement access control logic here
#         # Check user's role and determine access privileges
#         access_privileges = {
#             'SE_Data': 'Read/Write' if session['role'] == 'Admin' else 'No Access',
#             'HR_Data': 'Read/Write' if session['role'] == 'Admin' else 'No Access',
#             'PR_Data': 'Read/Write' if session['role'] == 'Admin' else 'No Access',
#             'Emp_SE': 'Read/Write' if session['role'] == 'Admin' else 'No Access',
#             'Emp_HR': 'Read/Write' if session['role'] == 'Admin' else 'No Access',
#             'Emp_PR': 'Read/Write' if session['role'] == 'Admin' else 'No Access',
#             'LogIn_Credential': 'Read/Write' if session['role'] == 'Admin' else 'No Access',
#             'SE_Data': 'Read/Write' if session['role'] == 'SE' else 'No Access',  # SE has read/write access, others have none
#             'Emp_SE': 'Read/Write' if session['role'] == 'SE' else 'No Access',   # SE has read/write access, others have none
#             'HR_Data': 'Read/Write' if session['role'] == 'HR' else 'No Access',
#             'Emp_HR': 'Read/Write' if session['role'] == 'HR' else 'No Access',
#             'Emp_PR': 'Read/Write' if session['role'] == 'HR' else 'No Access',
#             'Emp_SE': 'Read' if session['role'] == 'HR' else 'No Access',
#             'Emp_PR': 'Read/Write' if session['role'] == 'PR' else 'No Access',
#             'PR_Data': 'Read/Write' if session['role'] == 'PR' else 'No Access',
#             'Emp_SE': 'Read' if session['role'] == 'PR' else 'No Access',
#             'Emp_HR': 'Read' if session['role'] == 'PR' else 'No Access',
#             'Emp_SE': 'Read' if session['role'] == 'General' else 'No Access',
#             'Emp_HR': 'Read' if session['role'] == 'General' else 'No Access',
#             'Emp_PR': 'Read' if session['role'] == 'General' else 'No Access',
#             # Add more access privileges based on user's role
#         }
#         return render_template('dashboard.html', username=session['username'], role=session['role'], access_privileges=access_privileges)
#     app.logger.info('User accessed the home page')

#     return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        role = session['role']
        access_privileges = get_access_privileges_for_role(role)
        return render_template(
            'dashboard.html',
            username=session['username'],
            role=role,
            access_privileges=access_privileges
        )

    app.logger.info('User attempted to access dashboard without login')
    return redirect(url_for('login'))




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route('/add_login_credential')
def add_login_credential():
    return render_template('add_login_credential.html')
# Route for inserting data into LogIn_Credential table
@app.route('/insert_login_credential', methods=['POST'])
def insert_login_credential():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        cursor = db.cursor()
        cursor.execute("ALTER TABLE LogIn_Credential AUTO_INCREMENT = 1")  # Reset auto-increment counter

        # cursor.execute("INSERT INTO LogIn_Credential (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        cursor.execute("INSERT INTO LogIn_Credential (username, password, role) VALUES (%s, %s, %s)", (username, password, role))

        db.commit()
        flash('Data inserted into LogIn_Credential table successfully!', 'success')
        app.logger.info('User accessed the home page')
        return redirect(url_for('dashboard'))

# Route for rendering the form to add SE data
@app.route('/add_se_data')
def add_se_data():
    app.logger.info('User accessed the home page')
    return render_template('add_se_data.html')
    # if 'role' in session:
    #     role = session['role']
    #     if role == 'Admin' or role == 'SE':
    #         return render_template('add_se_data.html')
    # return redirect(url_for('login'))


# Route for inserting data into SE_Data table
@app.route('/insert_se_data', methods=['POST'])
def insert_se_data():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        projectname = request.form['projectname']
        supervisor = request.form['supervisor']
        deadline = request.form['deadline']

        cursor = db.cursor()
        cursor.execute("INSERT INTO SE_Data (id, name, projectname, supervisor, deadline) VALUES (%s, %s, %s, %s, %s)", (id, name, projectname, supervisor, deadline))
        db.commit()
        flash('Data inserted into SE_Data table successfully!', 'success')
        app.logger.info('User accessed the home page')
        return redirect(url_for('dashboard'))
    
# Route for rendering the form to add Emp_SE data
@app.route('/add_emp_se')
def add_emp_se():
    app.logger.info('User accessed the home page')
    return render_template('add_emp_se.html')
    # if 'role' in session:
    #     role = session['role']
    #     if role == 'Admin' or role == 'SE':
    #         return render_template('add_emp_se.html')
    # return redirect(url_for('login'))
   
# Route for inserting data into Emp_SE table
@app.route('/insert_emp_se', methods=['POST'])
def insert_emp_se():
    if request.method == 'POST':
        id = request.form['id']
        address = request.form['address']
        phone_no = request.form['phone_no']
        salary = request.form['salary']
        bloodgroup = request.form['bloodgroup']

        cursor = db.cursor()
        cursor.execute("INSERT INTO Emp_SE (id, address, phone_no, salary, bloodgroup) VALUES (%s, %s, %s, %s, %s)", (id, address, phone_no, salary, bloodgroup))
        db.commit()
        flash('Data inserted into Emp_SE table successfully!', 'success')
        app.logger.info('User accessed the home page')
        return redirect(url_for('dashboard'))


# Route for rendering the form to add HR data
@app.route('/add_hr_data')
def add_hr_data():
    app.logger.info('User accessed the home page')
    return render_template('add_hr_data.html')
    # if 'role' in session:
    #     role = session['role']
    #     if role == 'Admin' or role == 'HR':
    #         return render_template('add_hr_data.html')
    # return redirect(url_for('login'))


# Route for inserting data into HR_data table
@app.route('/insert_hr_data', methods=['POST'])
def insert_hr_data():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        department = request.form['department']
        supervisor = request.form['supervisor']

        cursor = db.cursor()
        cursor.execute("INSERT INTO HR_data (id, name, department, supervisor) VALUES (%s, %s, %s, %s)", (id, name, department, supervisor))
        db.commit()
        flash('Data inserted into HR_data table successfully!', 'success')
        app.logger.info('User accessed the home page')
        return redirect(url_for('dashboard'))



# Route for rendering the form to add Emp HR data
@app.route('/add_emp_hr')
def add_emp_hr():
    app.logger.info('User accessed the home page')
    return render_template('add_emp_hr.html')
    # if 'role' in session:
    #     role = session['role']
    #     if role == 'Admin' or role == 'HR':
    #         return render_template('add_emp_hr.html')
    # return redirect(url_for('login'))




# Route for inserting data into Emp_HR table
@app.route('/insert_emp_hr', methods=['POST'])
def insert_emp_hr():
    if request.method == 'POST':
        id = request.form['id']
        address = request.form['address']
        phone_no = request.form['phone_no']
        rank = request.form['rank']
        cursor = db.cursor()
        # cursor.execute("INSERT INTO Emp_HR (id, address, phone_no, rank) VALUES (%s, %s, %s, %s)", (id, address, phone_no, rank))
        cursor.execute("INSERT INTO Emp_HR (id, address, phone_no, emp_rank) VALUES (%s, %s, %s, %s)", (id, address, phone_no, rank))

        db.commit()
        flash('Data inserted into Emp_HR table successfully!', 'success')
        app.logger.info('User accessed the home page')
        return redirect(url_for('dashboard'))



# Route for rendering the form to add Emp HR data
@app.route('/add_emp_pr')
def add_emp_pr():
    app.logger.info('User accessed the home page')
    return render_template('add_emp_pr.html')
   


# Route for inserting data into Emp_PR table  add_emp_pr
@app.route('/insert_emp_pr', methods=['POST'])
def insert_emp_pr():
    if request.method == 'POST':
        id = request.form['id']
        address = request.form['address']
        phone_no = request.form['phone_no']
        salary = request.form['salary']

        cursor = db.cursor()
        cursor.execute("INSERT INTO Emp_PR (id, address, phone_no, salary) VALUES (%s, %s, %s, %s)", (id, address, phone_no, salary))
        db.commit()
        flash('Data inserted into Emp_PR table successfully!', 'success')
        app.logger.info('User accessed the home page')
        return redirect(url_for('dashboard'))



# Route for rendering the form to add Emp HR data
@app.route('/add_pr_data')
def add_pr_data():
    app.logger.info('User accessed the home page')
    return render_template('add_pr_data.html')
    # if 'role' in session:
    #     role = session['role']
    #     if role == 'Admin' or role == 'PR':
    #         return render_template('add_pr_data.html')
    # return redirect(url_for('login'))



# Route for inserting data into PR_Data table add_pr_data
@app.route('/insert_pr_data', methods=['POST'])
def insert_pr_data():
    if request.method == 'POST':
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = request.form['dob']

        cursor = db.cursor()
        cursor.execute("INSERT INTO PR_Data (id, firstname, lastname, dob) VALUES (%s, %s, %s, %s)", (id, firstname, lastname, dob))
        db.commit()
        flash('Data inserted into PR_Data table successfully!', 'success')
        app.logger.info('User accessed the home page')
        return redirect(url_for('dashboard'))

# New routes for viewing data
@app.route('/view_se_data')
def view_se_data():
    # Implement logic to fetch SE data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM SE_Data")
    se_data = cursor.fetchall()
    cursor.close()
    app.logger.info('User accessed the home page')
    return render_template('view_se_data.html', se_data=se_data)

@app.route('/view_hr_data')
def view_hr_data():
    # Implement logic to fetch HR data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM HR_data")
    hr_data = cursor.fetchall()
    cursor.close()
    app.logger.info('User accessed the home page')
    return render_template('view_hr_data.html', hr_data=hr_data)

@app.route('/view_emp_se')
def view_emp_se():
    # Implement logic to fetch Employee SE data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Emp_SE")
    emp_se_data = cursor.fetchall()
    cursor.close()
    app.logger.info('User accessed the home page')
    return render_template('view_emp_se.html', emp_se_data=emp_se_data)

# New routes for viewing data
@app.route('/view_emp_hr')
def view_emp_hr():
    # Implement logic to fetch Employee HR data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Emp_HR")
    emp_hr_data = cursor.fetchall()
    cursor.close()
    return render_template('view_emp_hr.html', emp_hr_data=emp_hr_data)

@app.route('/view_emp_pr')
def view_emp_pr():
    # Implement logic to fetch Employee PR data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Emp_PR")
    emp_pr_data = cursor.fetchall()
    cursor.close()
    app.logger.info('User accessed the home page')
    return render_template('view_emp_pr.html', emp_pr_data=emp_pr_data)

@app.route('/view_pr_data')
def view_pr_data():
    # Implement logic to fetch PR data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM PR_Data")
    pr_data = cursor.fetchall()
    cursor.close()
    app.logger.info('User accessed the home page')
    return render_template('view_pr_data.html', pr_data=pr_data)

@app.route('/view_login_credentials')
def view_login_credentials():
    # Implement logic to fetch Login Credential data from the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM LogIn_Credential")
    login_credentials = cursor.fetchall()
    cursor.close()
    app.logger.info('User accessed the home page')
    return render_template('view_login_credentials.html', login_credentials=login_credentials)

@app.route('/update_hr_data', methods=['GET', 'POST'])
def update_hr_data():
    app.logger.info('User accessed the home page')
    if request.method == 'POST':
        # Check if user is authenticated and authorized
        # if 'username' in session and session['role'] == 'HR':
        allowed_roles = ['Admin', 'HR']  # Specify roles allowed to update
        if 'username' in session and session['role'] in allowed_roles:
            # Get updated data from the form
            id = request.form['id']
            updated_data = {}

            # Iterate over form fields to collect updated data
            # for key, value in request.form.items():
            #     if key != 'id':
            #         updated_data[key] = value

            for key, value in request.form.items():
                if key == 'id':
                    continue
            # Map form field "rank" to DB column "emp_rank"
                if key == 'rank':
                    updated_data['emp_rank'] = value
                else:
                    updated_data[key] = value

            
            # Construct the SQL query dynamically
            set_clause = ', '.join([f"{key} = %s" for key in updated_data.keys()])
            query = f"UPDATE HR_Data SET {set_clause} WHERE id = %s"

            # Execute the query
            cursor = db.cursor()
            cursor.execute(query, list(updated_data.values()) + [id])
            db.commit()
            
            flash('HR data updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('dashboard'))
    else:
        # Render the update HR data template
        return render_template('update_hr_data.html')
    


@app.route('/update_se_data', methods=['GET', 'POST'])
def update_se_data():
    app.logger.info('User accessed the home page')
    if request.method == 'POST':
        # Check if user is authenticated and authorized
        # if 'username' in session and session['role'] == 'SE':
        allowed_roles = ['Admin', 'SE']  # Specify roles allowed to update
        if 'username' in session and session['role'] in allowed_roles:
            # Get updated data from the form
            id = request.form['id']
            updated_data = {}

            # Iterate over form fields to collect updated data
            for key, value in request.form.items():
                if key != 'id':
                    updated_data[key] = value
            
            # Construct the SQL query dynamically
            set_clause = ', '.join([f"{key} = %s" for key in updated_data.keys()])
            query = f"UPDATE SE_Data SET {set_clause} WHERE id = %s"

            # Execute the query
            cursor = db.cursor()
            cursor.execute(query, list(updated_data.values()) + [id])
            db.commit()
            
            flash('SE data updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('dashboard'))
    else:
        # Render the update HR data template
        return render_template('update_se_data.html')


@app.route('/update_pr_data', methods=['GET', 'POST'])
def update_pr_data():
    app.logger.info('User accessed the home page')
    if request.method == 'POST':
        # Check if user is authenticated and authorized
        # if 'username' in session and session['role'] == 'PR':
        allowed_roles = ['Admin', 'SE']  # Specify roles allowed to update
        if 'username' in session and session['role'] in allowed_roles:
            # Get updated data from the form
            id = request.form['id']
            updated_data = {}

            # Iterate over form fields to collect updated data
            for key, value in request.form.items():
                if key != 'id':
                    updated_data[key] = value
            
            # Construct the SQL query dynamically
            set_clause = ', '.join([f"{key} = %s" for key in updated_data.keys()])
            query = f"UPDATE PR_Data SET {set_clause} WHERE id = %s"

            # Execute the query
            cursor = db.cursor()
            cursor.execute(query, list(updated_data.values()) + [id])
            db.commit()
            
            flash('PR data updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('dashboard'))
    else:
        # Render the update HR data template
        return render_template('update_pr_data.html')


@app.route('/update_emp_pr', methods=['GET', 'POST'])
def update_emp_pr():
    app.logger.info('User accessed the home page')
    if request.method == 'POST':
        # Check if user is authenticated and authorized
        allowed_roles = ['Admin', 'HR', 'PR']  # Specify roles allowed to update

        if 'username' in session and session['role'] in allowed_roles:
            # Get updated data from the form
            id = request.form['id']
            updated_data = {}

            # Iterate over form fields to collect updated data
            for key, value in request.form.items():
                if key != 'id':
                    updated_data[key] = value
            
            # Construct the SQL query dynamically
            set_clause = ', '.join([f"{key} = %s" for key in updated_data.keys()])
            query = f"UPDATE Emp_PR SET {set_clause} WHERE id = %s"

            # Execute the query
            cursor = db.cursor()
            cursor.execute(query, list(updated_data.values()) + [id])
            db.commit()
            
            flash('PR data updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('dashboard'))
    else:
        # Render the update HR data template
        return render_template('update_emp_pr.html')
    
    
@app.route('/update_emp_se', methods=['GET', 'POST'])
def update_emp_se():
    app.logger.info('User accessed the home page')
    if request.method == 'POST':
        # Check if user is authenticated and authorized
        allowed_roles = ['Admin', 'SE']  # Specify roles allowed to update

        if 'username' in session and session['role'] in allowed_roles:
            # Get updated data from the form
            id = request.form['id']
            updated_data = {}

            # Iterate over form fields to collect updated data
            for key, value in request.form.items():
                if key != 'id':
                    updated_data[key] = value
            
            # Construct the SQL query dynamically
            set_clause = ', '.join([f"{key} = %s" for key in updated_data.keys()])
            query = f"UPDATE Emp_SE SET {set_clause} WHERE id = %s"

            # Execute the query
            cursor = db.cursor()
            cursor.execute(query, list(updated_data.values()) + [id])
            db.commit()
            
            flash('SE data updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('dashboard'))
    else:
        # Render the update HR data template
        return render_template('update_emp_se.html')
    


@app.route('/update_emp_hr', methods=['GET', 'POST'])
def update_emp_hr():
    app.logger.info('User accessed the home page')
    if request.method == 'POST':
        # Check if user is authenticated and authorized
        allowed_roles = ['Admin', 'HR']  # Specify roles allowed to update

        if 'username' in session and session['role'] in allowed_roles:
            # Get updated data from the form
            id = request.form['id']
            updated_data = {}

            # Iterate over form fields to collect updated data
            for key, value in request.form.items():
                if key != 'id':
                    updated_data[key] = value
            
            # Construct the SQL query dynamically
            set_clause = ', '.join([f"{key} = %s" for key in updated_data.keys()])
            query = f"UPDATE Emp_HR SET {set_clause} WHERE id = %s"

            # Execute the query
            cursor = db.cursor()
            try:
                cursor.execute(query, list(updated_data.values()) + [id])
                db.commit()
                flash('Employee (HR) data updated successfully!', 'success')
            except Exception as e:
                # Handle database errors
                flash('An error occurred while updating employee (HR) data.', 'error')
            finally:
                cursor.close()

            # Redirect to dashboard
            return redirect(url_for('dashboard'))
        else:
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('dashboard'))
    else:
        # Render the update HR data template
        return render_template('update_emp_hr.html')




@app.route('/update_role', methods=['POST'])
def update_role():
    if request.method == 'POST':
        # Get the form data
        employee_id = request.form.get('employee_id')
        new_role = request.form.get('new_role')

        # Update the role in the database (replace this with your database update logic)
        # Example:
        # db.update_role(employee_id, new_role)

        # For demonstration purposes, print the employee ID and new role to the console
        print(f"Updating role for employee ID {employee_id} to {new_role}")

        # Redirect back to the page displaying login credentials
        return redirect(url_for('view_login_credentials'))

#1. Flask route to delete an employee HR record
@app.route('/delete_emp_hr', methods=['POST'])
def delete_emp_hr():
    if request.method == 'POST':
        # Check if the user is authorized to perform the delete operation
        allowed_roles = ['Admin', 'HR']  # Specify roles allowed to delete
        if 'username' in session and session['role'] in allowed_roles:
            # Get the ID to delete from the form data
            id_to_delete = request.form.get('id')

            # Execute the SQL DELETE query to remove the record with the specified ID
            cursor = db.cursor()
            cursor.execute("DELETE FROM Emp_HR WHERE id = %s", (id_to_delete,))
            db.commit()

            # Flash a message to indicate successful deletion
            flash('Employee HR record deleted successfully!', 'success')

            # Redirect back to the view page
            return redirect(url_for('view_emp_hr'))
        else:
            # User is not authorized, display error message
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('view_emp_hr'))  # Redirect to a safe page or back to the dashboard
    else:
        # If the request method is not POST, return an error
        flash('Invalid request method.', 'error')
        return redirect(url_for('dashboard'))  # Redirect to a safe page or back to the dashboard


#2. Flask route to delete an employee PR record
@app.route('/delete_emp_pr', methods=['POST'])
def delete_emp_pr():
    if request.method == 'POST':
        # Check if the user is authorized to perform the delete operation
        allowed_roles = ['Admin', 'HR', 'PR']  # Specify roles allowed to delete
        if 'username' in session and session['role'] in allowed_roles:
            # Get the ID to delete from the form data
            id_to_delete = request.form.get('id')

            # Execute the SQL DELETE query to remove the record with the specified ID
            cursor = db.cursor()
            cursor.execute("DELETE FROM Emp_PR WHERE id = %s", (id_to_delete,))
            db.commit()

            # Flash a message to indicate successful deletion
            flash('Employee PR record deleted successfully!', 'success')

            # Redirect back to the view page
            return redirect(url_for('view_emp_pr'))
        else:
            # User is not authorized, display error message
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('view_emp_pr'))  # Redirect to a safe page or back to the dashboard
    else:
        # If the request method is not POST, return an error
        flash('Invalid request method.', 'error')
        return redirect(url_for('dashboard'))  # Redirect to a safe page or back to the dashboard



#3. Flask route to delete an employee SE record
@app.route('/delete_emp_se', methods=['POST'])
def delete_emp_se():
    if request.method == 'POST':
        # Check if the user is authorized to perform the delete operation
        allowed_roles = ['Admin', 'SE']  # Specify roles allowed to delete
        if 'username' in session and session['role'] in allowed_roles:
            # Get the ID to delete from the form data
            id_to_delete = request.form.get('id')

            # Execute the SQL DELETE query to remove the record with the specified ID
            cursor = db.cursor()
            cursor.execute("DELETE FROM Emp_SE WHERE id = %s", (id_to_delete,))
            db.commit()

            # Flash a message to indicate successful deletion
            flash('Employee SE record deleted successfully!', 'success')

            # Redirect back to the view page
            return redirect(url_for('view_emp_se'))
        else:
            # User is not authorized, display error message
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('view_emp_se'))  # Redirect to a safe page or back to the dashboard
    else:
        # If the request method is not POST, return an error
        flash('Invalid request method.', 'error')
        return redirect(url_for('dashboard'))  # Redirect to a safe page or back to the dashboard



#4. Flask route to delete an PR record
@app.route('/delete_pr_data', methods=['POST'])
def delete_pr_data():
    if request.method == 'POST':
        # Check if the user is authorized to perform the delete operation
        allowed_roles = ['Admin', 'PR']  # Specify roles allowed to delete
        if 'username' in session and session['role'] in allowed_roles:
            # Get the ID to delete from the form data
            id_to_delete = request.form.get('id')

            # Execute the SQL DELETE query to remove the record with the specified ID
            cursor = db.cursor()
            cursor.execute("DELETE FROM PR_Data WHERE id = %s", (id_to_delete,))
            db.commit()

            # Flash a message to indicate successful deletion
            flash('PR record deleted successfully!', 'success')

            # Redirect back to the view page
            return redirect(url_for('view_pr_data'))
        else:
            # User is not authorized, display error message
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('view_pr_data'))  # Redirect to a safe page or back to the dashboard
    else:
        # If the request method is not POST, return an error
        flash('Invalid request method.', 'error')
        return redirect(url_for('dashboard'))  # Redirect to a safe page or back to the dashboard



#5. Flask route to delete an PR record
@app.route('/delete_se_data', methods=['POST'])
def delete_se_data():
    if request.method == 'POST':
        # Check if the user is authorized to perform the delete operation
        allowed_roles = ['Admin', 'SE']  # Specify roles allowed to delete
        if 'username' in session and session['role'] in allowed_roles:
            # Get the ID to delete from the form data
            id_to_delete = request.form.get('id')

            # Execute the SQL DELETE query to remove the record with the specified ID
            cursor = db.cursor()
            cursor.execute("DELETE FROM SE_Data WHERE id = %s", (id_to_delete,))
            db.commit()

            # Flash a message to indicate successful deletion
            flash('SE record deleted successfully!', 'success')

            # Redirect back to the view page
            return redirect(url_for('view_se_data'))
        else:
            # User is not authorized, display error message
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('view_se_data'))  # Redirect to a safe page or back to the dashboard
    else:
        # If the request method is not POST, return an error
        flash('Invalid request method.', 'error')
        return redirect(url_for('dashboard'))  # Redirect to a safe page or back to the dashboard



#6. Flask route to delete an HR record
@app.route('/delete_hr_data', methods=['POST'])
def delete_hr_data():
    if request.method == 'POST':
        # Check if the user is authorized to perform the delete operation
        allowed_roles = ['Admin', 'HR']  # Specify roles allowed to delete
        if 'username' in session and session['role'] in allowed_roles:
            # Get the ID to delete from the form data
            id_to_delete = request.form.get('id')

            # Execute the SQL DELETE query to remove the record with the specified ID
            cursor = db.cursor()
            cursor.execute("DELETE FROM HR_Data WHERE id = %s", (id_to_delete,))
            db.commit()

            # Flash a message to indicate successful deletion
            flash('HR record deleted successfully!', 'success')

            # Redirect back to the view page
            return redirect(url_for('view_hr_data'))
        else:
            # User is not authorized, display error message
            flash('You are not authorized to perform this action.', 'error')
            return redirect(url_for('view_hr_data'))  # Redirect to a safe page or back to the dashboard
    else:
        # If the request method is not POST, return an error
        flash('Invalid request method.', 'error')
        return redirect(url_for('dashboard'))  # Redirect to a safe page or back to the dashboard


# @app.route('/update_user_role', methods=['POST'])
# def update_user_role():
#     if request.method == 'POST':
#         # Get the form data
#         username = request.form.get('username')
#         new_role = request.form.get('new_role')

#         # Check if the user is authorized to perform the update operation
#         allowed_roles = ['Admin']  # Adjust as needed
#         if session.get('role') not in allowed_roles:
#             flash('You do not have permission to update user roles.', 'error')
#             return redirect(url_for('view_login_credentials'))

#         # Execute the SQL UPDATE query to update the user's role
#         cursor = db.cursor()
#         cursor.execute("UPDATE LogIn_Credential SET role = %s WHERE username = %s", (new_role, username))
#         db.commit()

#         # Flash a message to indicate successful update
#         flash('User role updated successfully!', 'success')

#         # Redirect back to the view page
#         return redirect(url_for('view_login_credentials'))
#     else:
#         # Handle other HTTP methods if needed
#         pass


@app.route('/update_user_role', methods=['POST'])
def update_user_role():
    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username')
        new_role = request.form.get('new_role')

        # Check if the user is authorized to perform the update operation
        allowed_roles = ['Admin']  # Adjust as needed
        if session.get('role') not in allowed_roles:
            flash('You do not have permission to update user roles.', 'error')
            return redirect(url_for('view_login_credentials'))

        # Execute the SQL UPDATE query to update the user's role
        cursor = db.cursor()
        cursor.execute("UPDATE LogIn_Credential SET role = %s WHERE username = %s", (new_role, username))
        db.commit()

        # Return the updated role data as JSON response
        return jsonify({'username': username, 'new_role': new_role})
    else:
        # Handle other HTTP methods if needed
        pass



def serialize_role_row(row):
    # Adjust indexes to your table structure if needed
    return {
        "id": row[0],
        "username": row[1],
        "role": row[3],
    }

@app.route("/api/roles", methods=["GET"])
def api_get_roles():
    # TEMP: ignore DB, return mock data so frontend works
    mock_data = [
        {"id": 1, "username": "admin_user", "role": "Admin"},
        {"id": 2, "username": "se_user", "role": "SE"},
        {"id": 3, "username": "hr_user", "role": "HR"},
        {"id": 4, "username": "pr_user", "role": "PR"},
    ]
    return jsonify(mock_data), 200


# @app.route("/api/roles", methods=["GET"])
# def api_get_roles():
#     # If DB is not available, return mock data so frontend still looks good
#     if db is None:
#         app.logger.warning("DB is None; returning mock roles data.")
#         mock_data = [
#             {"id": 1, "username": "admin_user", "role": "Admin"},
#             {"id": 2, "username": "se_user", "role": "SE"},
#             {"id": 3, "username": "hr_user", "role": "HR"},
#         ]
#         return jsonify(mock_data), 200

#     cursor = db.cursor()
#     cursor.execute("SELECT id, username, password, role FROM LogIn_Credential")
#     rows = cursor.fetchall()
#     cursor.close()

#     data = [serialize_role_row(row) for row in rows]
#     return jsonify(data), 200

@app.route("/ping")
def ping():
    return "pong", 200




if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="127.0.0.1", port=8000, debug=True)






    