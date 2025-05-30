from flask import Flask, request, jsonify
from src.smart_kitchen_assistant.main import SmartKitchenAssistant
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    user = data["user"]
    response = SmartKitchenAssistant().run(user)
    
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
