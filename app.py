from flask import Flask, render_template, request, redirect

app = Flask(__name__)
todos = []  # List of dicts: [{'id': 1, 'task': 'Buy milk'}]
task_id = 1

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    global task_id
    task = request.form['task']
    todos.append({'id': task_id, 'task': task})
    task_id += 1
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    global todos
    todos = [t for t in todos if t['id'] != id]
    return redirect('/')

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    for i, t in enumerate(todos):
        if t['id'] == id:
            if request.method == 'POST':
                todos[i]['task'] = request.form['task']
                return redirect('/')
            return render_template('update.html', task=todos[i])
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
