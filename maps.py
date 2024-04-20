from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,text
from urllib.parse import quote
app = Flask(__name__)

# Encode the password
encoded_password = quote("groot@123", safe='')

# Configure MySQL database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@localhost/Lewis_schedule'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# Session = sessionmaker(bind=engine)
engine=create_engine(f'mysql+mysqlconnector://root:{encoded_password}@localhost/Lewis_schedule')
connection=engine.connect()
@app.route('/')
def index():
    return render_template('lewis_map.html')

@app.route('/schedule', methods=['POST'])
def show_schedule():
    campus = request.form['campus']
    instructor = request.form['instructor'] 
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    sql_query =text("SELECT * FROM course WHERE course.campus = :campus group by course.campus")

    # Execute the SQL query with parameters
    cursor=connection.execute(sql_query,{"campus":campus+' campus'})

    # Fetch all rows
    rows = cursor.fetchall()
    connection.close()

    return render_template('schedule.html', schedules=rows)

if __name__ == '__main__':
    app.run(debug=True)