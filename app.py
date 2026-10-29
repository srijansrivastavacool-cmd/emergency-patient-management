from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Task 1: Register patients and arrange them by emergency level and arrival number
patient = []
arrival_number = 0

# Task 2 and Task 6: Linked list of treated patients
class Node:
    def __init__(self, temp):
        self.patient_id = temp[0]
        self.name = temp[1]
        self.emergency_level = temp[2]
        self.arrival_time = temp[3]
        self.next = None

class Linkedlist:
    def __init__(self):
        self.head = None
        self.tail = None

    def linkedlist(self, newnode):
        if self.head is None:
            self.head = newnode
            self.tail = newnode
        else:
            self.tail.next = newnode
            self.tail = newnode

A = Linkedlist()

# Task 3: Build a normal binary tree from waiting patients
class Leaf:
    def __init__(self, patient_id):
        self.val = patient_id
        self.left = None
        self.right = None

class Formtree:
    def __init__(self):
        from collections import deque
        self.root = None
        queue = deque()
        for p in patient:
            newnode = Leaf(p[0])
            if not queue:
                self.root = newnode
                queue.append(newnode)
                continue
            current = queue[0]
            if current.left is None:
                current.left = newnode
            else:
                current.right = newnode
                queue.popleft()
            queue.append(newnode)

    def search(self, node, data):
        if node is None:
            return False
        if node.val == data:
            return True
        return self.search(node.left, data) or self.search(node.right, data)

@app.route('/')
def home():
    return render_template('index.html')

@app.get('/api/state')
def state():
    treated = []
    current = A.head
    while current is not None:
        treated.append({
            'patient_id': current.patient_id,
            'name': current.name,
            'emergency_level': current.emergency_level,
            'arrival_time': current.arrival_time
        })
        current = current.next
    return jsonify({'waiting': patient, 'treated': treated})

@app.post('/api/register')
def register_new_patient():
    global arrival_number
    data = request.get_json(silent=True) or {}
    try:
        patient_id = int(data.get('patient_id'))
        emergency_level = int(data.get('emergency_level'))
    except (TypeError, ValueError):
        return jsonify({'message': 'Enter a valid patient ID and emergency level.'}), 400

    name = str(data.get('name', '')).strip()
    if not name:
        return jsonify({'message': 'Enter patient name.'}), 400
    if any(p[0] == patient_id for p in patient):
        return jsonify({'message': 'This patient ID is already waiting.'}), 400
    if emergency_level < 1 or emergency_level > 5:
        return jsonify({'message': 'Emergency level must be from 1 to 5.'}), 400

    arrival_number += 1
    patient.append([patient_id, name, emergency_level, arrival_number])
    patient.sort(key=lambda x: (-x[2], x[3]))
    return jsonify({'message': 'Patient registered successfully.'})

@app.post('/api/treat')
def treat_patient():
    if not patient:
        return jsonify({'message': 'No patients waiting.'}), 400
    temp = patient.pop(0)
    A.linkedlist(Node(temp))
    return jsonify({'message': 'Patient treated successfully.'})

@app.get('/api/search')
def search_a_patient():
    try:
        target = int(request.args.get('patient_id', ''))
    except ValueError:
        return jsonify({'message': 'Enter a valid patient ID.'}), 400
    tree = Formtree()
    if tree.search(tree.root, target):
        return jsonify({'message': 'Patient found in the waiting list.'})
    return jsonify({'message': 'Patient not found in the waiting list.'}), 404

@app.delete('/api/cancel/<int:target>')
def cancel_registration(target):
    for i in range(len(patient)):
        if patient[i][0] == target:
            patient.pop(i)
            return jsonify({'message': 'Registration cancelled.'})
    return jsonify({'message': 'Patient not found in the waiting list.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
