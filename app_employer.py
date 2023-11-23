from flask import Flask, render_template, url_for, request, redirect
from flask import session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "DBMS"

# Configure Database
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "3010"
app.config['MYSQL_DB'] = "job_application"

mysql = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def login():
    find = 0
    if request.method == 'POST':
        # retrieving the entries made in the login form
        loginDetails = request.form
        email = loginDetails['email']
        password = loginDetails['password']
        cur = mysql.connection.cursor()
        
        find = cur.execute("SELECT * FROM employer WHERE (email, password) = (%s, %s) ", (email, password))
        details = cur.fetchall()
        cur.close()
    # login to home page if we find such an entry in the table or redirect to the same page
    if find != 0:
        user = details[0][0]
        session["user"] = user
        print(user)
        return redirect('/employer_home')
    else: 
        if "user" in session:
            return redirect(url_for("employer_home"))
        return render_template('employer_login.html', find = find)

@app.route('/employer_signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # retrieving the entries made in the signup form
        userDetails = request.form
        fname = userDetails['fname']
        lname = userDetails['lname']
        phone_num = userDetails['phone_num']
        email = userDetails['email']
        password = userDetails['password']
        cpassword = userDetails['cpassword']
        c_id = int(userDetails['company_id'])
        # checking if the password entered in both the fields are same
        if password == cpassword:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO employer(first_name, last_name, phone_number, email, password, company_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (fname, lname, phone_num, email, password, c_id))
            mysql.connection.commit()
            cur.close()
            # go to login page on submit
            return redirect('/')
        else:
            return redirect('employer_signup')
    return render_template('employer_signup.html')

@app.route('/employer_home', methods = ['GET', 'POST'])
def employer_home():
    if "user" in session:
        user = session["user"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employer WHERE employer_id = {}".format(user))
        userdet = cur.fetchall()
        name = userdet[0][1]
        return render_template('employer_home.html', name = name)
    else:
        return redirect(url_for('employer_login'))
@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT jobseeker.first_name, jobseeker.last_name, jobseeker.email, job.job_type, job.job_id \
                     FROM jobseeker INNER JOIN apply ON jobseeker.jobseeker_id = apply.jobseeker_id \
                     INNER JOIN job ON apply.job_id = job.job_id\
                     INNER JOIN employer on employer.company_id=job.company_id;")
        application_details = cur.fetchall()
        cur.close()
        return render_template('employer_jobs.html', application_details=application_details)
    
    # If the user is not in the session or the request method is not POST, redirect to the login page
    return redirect(url_for('employer_home'))

@app.route('/employer_accept_reject', methods=['POST'])
def employer_accept_reject():
    if "user" in session and request.method == 'POST':
        user = session["user"]
        job_id = request.form['job_id']
        action = request.form['action']

        # You need to implement the logic to update the Status in the result table based on the action (Accept/Reject)
        cur = mysql.connection.cursor()
        
        try:
            cur.execute("UPDATE result SET status = %s WHERE job_id = %s", (action, job_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('jobs'))
        except Exception as e:
            print("Error updating result table:", str(e))
            cur.close()
            return redirect(url_for('jobs'))
    # If the user is not in the session or the request method is not POST, redirect to the login page
    return redirect(url_for('employer_home'))

@app.route('/interviews')
def interviews():
    if "user" in session:
        user = session['user']
        cur = mysql.connection.cursor()
        # select all the interview details for those jobs that the user has applied for by using inner join on apply and interview's job_id
        check_apply = cur.execute("select job.job_title, interview.date, interview.time FROM\
            interview inner join job on job.job_id=interview.job_id\
            inner join employer on employer.company_id=job.company_id where employer.employer_id={};".format(user))
        if check_apply > 0:
            # select the interview details, its corresponding job and company details by using inner join on job, company and interview
            # and using subquery to show interview schedules for only those jobs that the jobseeker has applied for
            interview = cur.execute("select job.job_title, interview.date, interview.time FROM\
            interview inner join job on job.job_id=interview.job_id\
            inner join employer on employer.company_id=job.company_id where employer.employer_id={};".format(user))
            if interview > 0:
                schedule = cur.fetchall()
            else:
                schedule = None
        else:
            schedule = None
        return render_template('employer_interview.html', schedule=schedule)
    else:
        return redirect(url_for('employer_login')) 
    
@app.route('/execute_query', methods=['POST'])
def execute_query():
    if request.method == 'POST':
        sql_query = request.form['sql_query']

        try:
            # Assuming you have a database connection named 'mysql'
            cur = mysql.connection.cursor()
            cur.execute(sql_query)
            mysql.connection.commit()

            # Fetch the result after executing the query
            result = cur.fetchall()

            cur.close()

            # Return the result as a string
            result_str = "\n".join([str(row) for row in result])
            return result_str

        except Exception as e:
            return f"Error executing query: {str(e)}"

    return "Invalid request method."

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True,port=5001)