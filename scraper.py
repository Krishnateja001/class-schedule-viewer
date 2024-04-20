
import csv
import sqlite3
from bs4 import BeautifulSoup


conn = sqlite3.connect('class_schedule.db')
c = conn.cursor()

# Create a table to store the class schedule data
c.execute('''CREATE TABLE IF NOT EXISTS class_schedule
             (course_name TEXT, course_code TEXT, section TEXT, term TEXT, registration_dates TEXT, level TEXT, campus TEXT, schedule_type TEXT, instructional_method TEXT, credits REAL, catalog_link TEXT, schedule_data TEXT)''')


def schedule_data(course_code,schedule_table):
    if schedule_table:
        # Initialize an empty list to store the schedule data
        schedule_data = []

        # Find all <tr> elements within the table
        rows = schedule_table.find_all('tr')

        # Iterate over each row (skipping the first row which contains headers)
        for row in rows[1:]:
            # Extract the data from each cell (<td>) in the row
            cells = row.find_all('td')
            
            # Extracting values from each cell and assigning them to variables
            type_value = cells[0].get_text(strip=True)
            time_value = cells[1].get_text(strip=True)
            days_value = cells[2].get_text(strip=True)
            where_value = cells[3].get_text(strip=True)
            date_range_value = cells[4].get_text(strip=True)
            schedule_type_value = cells[5].get_text(strip=True)
            instructors_value = cells[6].get_text(strip=True)

            # Append the row data to the schedule_data list
            schedule_data.append([type_value, time_value, days_value, where_value, date_range_value, schedule_type_value, instructors_value])
            # yield schedule_data
    else:
        schedule_data = []
    return schedule_data


with open('classschedule/fall_2024.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the course sections
course_titles = soup.find_all('th', class_='ddtitle')

course_table=soup.find('table', class_='datadisplaytable')
rows=course_table.find_all('tr')

# there are two rows for every class data first row class= ddtitle has heading and second table row class=ddefault has span and br tags with a another table class='datadisplaytable' which has schedule with multiple rows

tr_elements = soup.find_all('tr')
print(len(tr_elements))
i=0
response=[]
# Loop through each <tr> element
for tr_element in tr_elements:
    # Find the <th> element with the class 'ddtitle' inside the <tr>
    section_th = tr_element.find('th', {'class': 'ddtitle'})

    if section_th:
        # Extract the course details
        course_details = section_th.a.text.split(' - ')
        course_name = course_details[0]
        course_code = course_details[1]
        try:
            course_code=int(course_code)
            section_code = course_details[2]
        except ValueError:
            # print(course_details)
            course_code=course_details[2]
            section_code = course_details[3]
        

        # Find the next sibling <tr> element containing the course information
        course_info_row = tr_element.find_next_sibling('tr')

        if course_info_row:
            course_info = course_info_row.find('td', {'class': 'dddefault'})
            campus = course_info.find(string=lambda string: string and 'Campus' in string).strip()
            schedule_type = course_info.find(string=lambda string: string and 'Schedule Type' in string).strip()
            instructional_method = course_info.find(string=lambda string: string and 'Instructional Method' in string).strip()
            credits_text = course_info.find(string=lambda string: string and 'Credits' in string).strip()
            level=course_info.find(string=lambda string: string and 'raduate' in string).strip()
            registration_dates=course_info.find(string=lambda string: string and 'to' in string).strip()
            credits = credits_text.split(' ')[0] if credits_text else None
            # catalog_link = course_info.find('a', href=True)['href'] if course_info.find('a', href=True) else None

            # Find the schedule data table
            schedule_table = course_info.find('table', {'class': 'datadisplaytable'})
            
            schedule_data_ = schedule_data(course_code,schedule_table)

            # print(schedule_data_)
        for row in schedule_data_:
            total_data=[course_name, course_code, section_code,'Fall-2024',registration_dates,level,credits, campus, schedule_type, instructional_method]

            total_data.extend(row)

        # break
            response.append(total_data)


def store_output():
    with open('output/output_fall_2024.csv', 'w', newline='') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)
        column_list = [
    'course_name', 'course_code', 'section', 'Fall-2024','registration_dates','level','credit', 'campus', 
    'schedule_type', 'instructional_method', 'type', 'time', 'days', 
    'location', 'date_range', 'lecture_type', 'instructors']
        response.insert(0,column_list)
        # Iterate through the list of lists
        for row in response:
            if len(row)==len(column_list):
                # print(column_list,row)

                csv_writer.writerow(row)
            else:
                print(column_list,row)
                print('error')

        # ,columns=['course_name', 'course_code', 'section_code', 'term', 'registration_dates', 'level', 'campus', 'schedule_type', 'instructional_method','schedule_data'])


# store_output()