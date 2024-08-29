import psycopg2 as ps
from random import randint, choice
from data import *
def insert_employee (cursor, values):
    query = '''INSERT INTO employees (name, age, department)
    VALUES (%s, %s, %s)'''
    cursor.execute(query, values)

def select_records(cursor):
    query = '''SELECT * FROM employees'''
    cursor.execute(query)
    return cursor.fetchall()

def random_name():
    name = choice(random_names)
    surname = choice(random_surnames)
    return f'{name} {surname}'

conn = None
try:
    conn = ps.connect(
        dbname="company",
        user="postgres",
        password="password",
        host="db",
        port="5432"
    )

    cur = conn.cursor()

    count_records = randint(8,15)
    for _ in range(count_records):
        employee_name = random_name()
        employee_age = randint(18,45)
        employee_department = choice(random_departments)
        insert_employee(cur, (employee_name,employee_age, employee_department))
    conn.commit()

    employees_list = select_records(cur)
    keys = ['id', 'name', 'age', 'department']
    employees_list = [dict(zip(keys, values)) for values in employees_list]
    for employee in employees_list:
        print(', '.join(f"{key}: {value}" for key, value in employee.items()))

except (Exception, ps.Error) as error:
    print(error)


finally:
    if conn:
        conn.close()
