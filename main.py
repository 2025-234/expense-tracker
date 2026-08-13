from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    # Logique de calcul ou d'enregistrement
    total = data.get('amount', 0) * 1.1  # Exemple de calcul
    return jsonify({"status": "success", "total_with_tax": total})

if __name__ == '__main__':
    app.run(debug=True)
