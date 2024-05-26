from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 # pip install psycopg2 
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "Trung-Nguyen"

DB_HOST = "localhost"
DB_NAME = "databaseCURD"
DB_USER = "postgres"
DB_PASS = "trung253"

conn =  psycopg2.connect( dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)

@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        cur.execute("INSERT INTO students (firstName, lastName, email) VALUES (%s,%s,%s)", (firstName,lastName,email))
        conn.commit()
        flash("Student Added Successfully!")
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST','GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM students WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE students
            SET firstName = %s,
                lastName = %s,
                email = %s
            WHERE id = %s
        """, (firstName, lastName, email, id))
        flash('Updated Successfully!')
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    conn.commit()
    flash('Removed Successfully!')
    return redirect(url_for('Index'))
    
if __name__ == "__main__":
    app.run(debug=True)