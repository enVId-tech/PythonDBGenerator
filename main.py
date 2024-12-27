import sqlite3
import random
from datetime import datetime, timedelta
import string
import os
import time

ROWS = 20
RUNTIMES = 5
TTW = 1 # Time to wait in seconds, numbers less than 1 will result in override issues

def create_sample_database():
    # Connect to SQLite database (creates a new one if it doesn't exist)
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()

    # Create table with 10 columns of different types
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sample_data (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        salary REAL,
        date_joined DATE,
        email TEXT,
        department TEXT,
        is_active BOOLEAN,
        rating REAL,
        comments TEXT
    )
    ''')

    # List of sample departments and domains for random selection
    departments = ['Sales', 'Marketing', 'Engineering', 'HR', 'Finance']
    domains = ['example.com', 'company.net', 'business.org', 'corp.com']

    # Generate 20 rows of random data
    for i in range(ROWS):
        # Generate random name
        first_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))
        last_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8))
        name = f"{first_name} {last_name}"
        
        # Generate random age between 22 and 65
        age = random.randint(22, 65)
        
        # Generate random salary between 30000 and 120000
        salary = round(random.uniform(30000, 120000), 2)
        
        # Generate random date within last 5 years
        start_date = datetime.now() - timedelta(days=5*365)
        random_days = random.randint(0, 5*365)
        date_joined = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        # Generate random email
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        
        # Random department
        department = random.choice(departments)
        
        # Random boolean for is_active
        is_active = random.choice([0, 1])
        
        # Random rating between 1 and 5
        rating = round(random.uniform(1, 5), 1)
        
        # Random comment
        comments = ''.join(random.choices(string.ascii_letters + ' ', k=50))

        # Insert the data
        cursor.execute('''
        INSERT INTO sample_data (name, age, salary, date_joined, email, department, is_active, rating, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, salary, date_joined, email, department, is_active, rating, comments))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

for i in range(RUNTIMES):
	time.sleep(TTW)

	# Create the database
	create_sample_database()

	# Verify the data (optional)

	# Create sample.db files based on how many times the script is run
	conn = sqlite3.connect('sample.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM sample_data')
	rows = cursor.fetchall()
	
	# Print the data

	print(f"Sample database created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	for row in rows:
		print(row)

	print(f"Total rows: {len(rows)}")
	print(f"Run time: {i*TTW}")
	print(f"Run number: {i+1}\n")
	print("===========================================\n")
	
	conn.close()

	if os.path.exists('sample.db'):
		os.rename('sample.db', f'sample_{datetime.now().strftime("%Y%m%d%H%M%S")}.db')