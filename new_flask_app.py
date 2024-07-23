from flask import Flask, request, jsonify
from new_agent import agent, query_agent, get_db  # Ensure these imports are correct

app = Flask(__name__)

# Initialize the agent with your API key and database connection
api_key = "YOUR API KEY"

try:
    db = get_db()  # Ensure this function correctly initializes your database
    # Initialize your agent here if needed
except Exception as e:
    app.logger.error("Failed to initialize the agent: %s", str(e))
    agent = None

@app.route('/query', methods=['POST'])
def query():
    if not agent:
        return jsonify({"response": "Agent not initialized"}), 500

    input_data = request.json
    if not input_data or "question" not in input_data:
        return jsonify({"response": "Invalid input"}), 400

    question = input_data.get("question", "")
    try:
        response = query_agent(agent, question)
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error("Error querying agent: %s", str(e))
        return jsonify({"response": "Error querying agent"}), 500




if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)  # Expose the server on all network interfaces
