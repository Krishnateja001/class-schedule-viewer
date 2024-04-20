from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
from datetime import datetime
import pandas as pd
from urllib.parse import quote
from io import StringIO

app = Flask(__name__)



# Encode the password
encoded_password = quote("groot@123", safe='')

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@localhost/Lewis_schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Model for your table
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    course_code = db.Column(db.String(50))
    section = db.Column(db.String(10))
    semester=db.Column(db.String(15))
    registration_dates=db.Column(db.String(50))
    level=db.Column(db.String(15))
    credit = db.Column(db.Integer)
    campus = db.Column(db.String(100))
    schedule_type = db.Column(db.String(100))
    instructional_method = db.Column(db.String(100))
    type = db.Column(db.String(50))
    start_time = db.Column(db.DateTime)  # Change to DateTime type
    end_time = db.Column(db.DateTime)    # Change to DateTime type
    days = db.Column(db.String(50))
    location = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    lecture_type = db.Column(db.String(100))
    instructors = db.Column(db.String(255))

# Route for uploading CSV file
@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return render_template('upload.html', error='No file part')
        
        file = request.files['file']
        
        # Check if file is CSV
        if file.filename == '':
            return render_template('upload.html', error='No selected file')
        
        if file and file.filename.endswith('.csv'):
            # Read CSV data and store it in MySQL
            stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_data = csv.reader(stream)
            next(csv_data)  # Skip header
            for row in csv_data:
                if row[11] !='TBA' and row[11]:
                    start_time, end_time = row[11].split('-')
                else:
                    start_time, end_time = (None, None)
                    
                start_date, end_date = row[14].split(' - ') if row[14] else (None, None)
                course = Course(
                    course_name=row[0],
                    course_code=row[1],
                    section=row[2],
                    semester=row[3],
                    registration_dates=row[4],
                    level=row[5],
                    credit=row[6],
                    campus=row[7],
                    schedule_type=row[8],
                    instructional_method=row[9],
                    type=row[10],
                    start_time=datetime.strptime(start_time.strip(), '%I:%M %p') if start_time else None,  # Convert to datetime
                    end_time=datetime.strptime(end_time.strip(), '%I:%M %p')if end_time else None,      # Convert to datetime
                    days=row[12],
                    location=row[13],
                    start_date=pd.to_datetime(start_date.strip(), format='%b %d, %Y') if start_date else None,
                    end_date=pd.to_datetime(end_date.strip(), format='%b %d, %Y') if end_date else None,
                    lecture_type=row[15],
                    instructors=row[16]
                )

                db.session.add(course)
                db.session.commit()

            return 'CSV file uploaded successfully and data stored in MySQL database'
        else:
            return render_template('upload.html', error='Please upload a CSV file')
    
    return render_template('upload.html')

# if __name__ == '__main__':
#     app.run(debug=True)

