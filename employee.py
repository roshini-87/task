from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace 'postgresql://user:password@localhost/dbname' with your actual PostgreSQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Employee model for the database
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(50), nullable=False)

# Define a route to get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    # Query all employees from the database
    employees = Employee.query.all()
    
    # Create a list of dictionaries containing employee details
    employee_list = [{'id': emp.id, 'name': emp.name, 'designation': emp.designation} for emp in employees]
    
    # Return the list of employees as JSON
    return jsonify({'employees': employee_list})

# Define a route to get a specific employee by ID
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    # Query an employee by ID from the database
    employee = Employee.query.get(employee_id)
    
    # Check if the employee exists
    if employee:
        # Return the employee details as JSON
        return jsonify({'id': employee.id, 'name': employee.name, 'designation': employee.designation})
    else:
        # Return an error response if the employee is not found
        return jsonify({'error': 'Employee not found'}), 404

# Define a route to add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    # Get JSON data from the request
    data = request.get_json()

    # Extract name and designation from the JSON data
    name = data.get('name')
    designation = data.get('designation')

    # Create a new Employee object
    new_employee = Employee(name=name, designation=designation)
    
    # Add the new employee to the database
    db.session.add(new_employee)
    db.session.commit()

    # Return a success response with the new employee's ID
    return jsonify({'message': 'Employee added successfully', 'id': new_employee.id}), 201

# Define a route to update an existing employee by ID
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    # Query an employee by ID from the database
    employee = Employee.query.get(employee_id)

    # Check if the employee exists
    if not employee:
        # Return an error response if the employee is not found
        return jsonify({'error': 'Employee not found'}), 404

    # Get JSON data from the request
    data = request.get_json()
    
    # Update the employee's name and designation if provided in the JSON data
    employee.name = data.get('name', employee.name)
    employee.designation = data.get('designation', employee.designation)

    # Commit the changes to the database
    db.session.commit()

    # Return a success response with the updated employee's ID
    return jsonify({'message': 'Employee updated successfully', 'id': employee.id})

# Define a route to delete an existing employee by ID
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    # Query an employee by ID from the database
    employee = Employee.query.get(employee_id)

    # Check if the employee exists
    if not employee:
        # Return an error response if the employee is not found
        return jsonify({'error': 'Employee not found'}), 404

    # Delete the employee from the database
    db.session.delete(employee)
    db.session.commit()

    # Return a success response
    return jsonify({'message': 'Employee deleted successfully'})

# Run the application in debug mode
if __name__ == '__main__':
    # Create the database tables before running the app
    db.create_all()
    
    # Run the Flask application
    app.run(debug=True)
