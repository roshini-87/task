from flask import Flask, request, jsonify

app = Flask(__name__)

# Initial net amount in the bank account
net_amount = 5000

@app.route('/compute_net_amount', methods=['POST'])
def compute_net_amount():
    
    # Get JSON data from the request
    data = request.get_json()
    
    # Check if required keys are present in the JSON data
    if 'net_amount' not in data or 'mode' not in data or 'amount' not in data:
        return jsonify({'error': 'Invalid input format'}), 400
    
    # Extract values from the JSON data
    mode = data['mode'].lower()
    amount = data['amount']

    global net_amount

    # Perform deposit or withdrawal based on the transaction mode
    if mode == 'deposit':
        net_amount += amount
    elif mode == 'withdraw':
        net_amount -= amount
    else:
        return jsonify({'error': 'Invalid transaction mode'}), 400
    
    # Return the updated net amount in the response
    return jsonify({'net_amount': net_amount})

if __name__ == '__main__':
    app.run(debug=True)