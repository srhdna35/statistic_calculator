from flask import Flask, render_template, request, redirect, url_for
import statistics
import json
import os
import uuid
import numpy as np  # Tambahkan untuk menghitung kuartil
from collections import Counter, defaultdict
from flask import render_template, request

app = Flask(__name__)

HISTORY_FILE = 'history.json'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route("/result", methods=["POST"])
def result():
    try:
        data = request.form.get("expenses")
        if not data:
            return redirect("/calculator")

        expenses = json.loads(data)
        amounts = [int(item["amount"]) for item in expenses]

        categories = list(set(item["category"] for item in expenses))
        category_totals = {
            category: sum(int(item["amount"]) for item in expenses if item["category"] == category)
            for category in categories
        }

        return render_template("result.html",
            total=sum(amounts),
            mean=statistics.mean(amounts),
            median=statistics.median(amounts),
            mode=statistics.mode(amounts),
            minimum=min(amounts),
            maximum=max(amounts),
            range_value=max(amounts) - min(amounts),
            stdev=statistics.stdev(amounts) if len(amounts) > 1 else 0,
            count=len(amounts),
            categories=categories,
            q1=statistics.quantiles(amounts, n=4)[0],
            q2=statistics.median(amounts),
            q3=statistics.quantiles(amounts, n=4)[2],
            expenses=expenses,
            chart_labels=list(category_totals.keys()),
            chart_values=list(category_totals.values())
        )
    except Exception as e:
        return f"Error: {e}"


@app.route('/history')
def history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history_data = json.load(f)
    else:
        history_data = []

    return render_template('history.html', history=history_data)

@app.route('/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    target_item = None
    for session in history:
        for item in session:
            if item.get('id') == item_id:
                target_item = item
                break

    if not target_item:
        return "Item not found", 404

    if request.method == 'POST':
        target_item['amount'] = request.form['amount']
        target_item['category'] = request.form['category']

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)

        return redirect(url_for('history'))

    return render_template('edit.html', item=target_item)

def save_to_history(entry):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    else:
        history = []

    history.append(entry)

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
