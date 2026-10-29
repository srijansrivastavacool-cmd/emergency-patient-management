# Emergency Patient Management System (Simple Model)

This is a simple web model based on the six tasks in the supplied Python code:

1. Register a patient and sort waiting patients by emergency level, then arrival order.
2. Treat the next patient and add the patient to a linked list.
3. Search for a patient in a normal binary tree built from the waiting list.
4. Display waiting patients.
5. Cancel a waiting patient's registration.
6. Display treated patients from the linked list.

## Run it

1. Install Python.
2. Open a terminal in this folder.
3. Install Flask:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   python app.py
   ```
5. Open the local address shown in the terminal (usually http://127.0.0.1:5000).

Data is kept in memory, so it resets when the server is stopped. This is a college-project demonstration, not a production medical system.
