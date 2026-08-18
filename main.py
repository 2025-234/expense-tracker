import os
import csv
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

# Stockage des dépenses en mémoire
expenses = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        amount = request.form.get('amount')
        category = request.form.get('category')
        
        if title and amount and category:
            expenses.append({
                'id': len(expenses) + 1,
                'title': title, 
                'amount': float(amount), 
                'category': category
            })
            
        return redirect(url_for('home'))

    total = sum(e['amount'] for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/delete/<int:expense_id>')
def delete(expense_id):
    global expenses
    expenses = [e for e in expenses if e['id'] != expense_id]
    return redirect(url_for('home'))

@app.route('/export')
def export_csv():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Titre', 'Montant', 'Categorie'])
    for e in expenses:
        cw.writerow([e['id'], e['title'], e['amount'], e['category']])
        
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=depenses.csv"}
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
