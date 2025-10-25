from flask import Flask, render_template, request, jsonify
from algorithms import sorting

app = Flask(__name__)

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for visualize page
@app.route('/visualize')
def visualize():
    algo = request.args.get('algo')
    data_str = request.args.get('data')
    return render_template('visualize.html', algo=algo, data=data_str)

# API endpoint to fetch sorting steps
@app.route('/get_steps')
def get_steps():
    algo = request.args.get('algo')
    data_str = request.args.get('data')
    
    if not data_str:
        return jsonify({'error': 'No data provided'}), 400

    try:
        arr = [int(x.strip()) for x in data_str.split(',')]
    except ValueError:
        return jsonify({'error': 'Invalid dataset format'}), 400

    # Select sorting algorithm
    if algo == 'bubble':
        gen = sorting.bubble_sort_steps(arr)
    elif algo == 'selection':
        gen = sorting.selection_sort_steps(arr)
    elif algo == 'insertion':
        gen = sorting.insertion_sort_steps(arr)
    elif algo == 'quick':
        gen = sorting.quick_sort_steps(arr)
    elif algo == 'merge':
        gen = sorting.merge_sort_steps(arr)
    else:
        return jsonify({'error': 'Invalid algorithm'}), 400

    steps = [step for step in gen]
    return jsonify({'steps': steps})

if __name__ == '__main__':
    app.run(debug=True)
