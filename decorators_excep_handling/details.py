from flask import Flask, request, jsonify
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/roshini'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Employee model
class Employee_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(50), nullable=False)

# Create tables in the database
db.create_all()

# Decorator to log API calls
def log_api_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"API call: {request.method} {request.url}")
        return func(*args, **kwargs)
    return wrapper

# Decorator for exception handling
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return wrapper

# GET API to retrieve all employees
@app.route('/employee_details', methods=['GET'])
@log_api_call
@handle_exceptions
def get_employees():
    employees = Employee_details.query.all()
    employee_list = [{"id": emp.id, "name": emp.name, "age": emp.age, "position": emp.position} for emp in employees]
    return jsonify(employee_list)

# GET API to retrieve a specific employee
@app.route('/employee_deatils/<int:employee_id>', methods=['GET'])
@log_api_call
@handle_exceptions
def get_employee(employee_id):
    employee = Employee_details.query.get(employee_id)
    if employee:
        return jsonify({"id": employee.id, "name": employee.name, "age": employee.age, "position": employee.position})
    else:
        raise ValueError(f"Employee with ID {employee_id} not found")

# POST API to add a new employee
@app.route('/employee_details', methods=['POST'])
@log_api_call
@handle_exceptions
def add_employee():
    data = request.get_json()
    new_employee = Employee_details(name=data['name'], age=data['age'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": f"Employee added with ID {new_employee.id}"}), 201

# PUT API to update employee details
@app.route('/employee_details/<int:employee_id>', methods=['PUT'])
@log_api_call
@handle_exceptions
def update_employee(employee_id):
    employee = Employee_details.query.get(employee_id)
    if employee:
        data = request.get_json()
        employee.name = data['name']
        employee.age = data['age']
        employee.position = data['position']
        db.session.commit()
        return jsonify({"message": f"Employee with ID {employee_id} updated"})
    else:
        raise ValueError(f"Employee with ID {employee_id} not found")

# DELETE API to delete an employee
@app.route('/employee_details/<int:employee_id>', methods=['DELETE'])
@log_api_call
@handle_exceptions
def delete_employee(employee_id):
    employee = Employee_details.query.get(employee_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": f"Employee with ID {employee_id} deleted"})
    else:
        raise ValueError(f"Employee with ID {employee_id} not found")

if __name__ == '__main__':
    app.run(debug=True)
