from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['GET'])
def add_numbers():
    try:
        # Get parameters 'a' and 'b' from the query string
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))

        # Calculate the sum
        result = a + b

        # Return the result as JSON
        return jsonify({'result': result})

    except ValueError:
        # Handle the case where 'a' or 'b' is not a valid integer
        return jsonify({'error': 'Invalid input. Please provide valid integers for parameters "a" and "b".'}), 400

if __name__ == '__main__':
    app.run(debug=True)
