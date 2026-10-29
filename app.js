const message = document.getElementById('message');

async function refreshLists() {
  const response = await fetch('/api/state');
  const data = await response.json();
  const waitingBody = document.getElementById('waiting-list');
  const treatedBody = document.getElementById('treated-list');
  waitingBody.innerHTML = '';
  treatedBody.innerHTML = '';

  data.waiting.forEach(p => {
    const row = document.createElement('tr');
    [p[0], p[1], p[2], p[3]].forEach(value => {
      const cell = document.createElement('td');
      cell.textContent = value;
      row.appendChild(cell);
    });
    const action = document.createElement('td');
    const cancel = document.createElement('button');
    cancel.textContent = 'Cancel';
    cancel.addEventListener('click', () => cancelPatient(p[0]));
    action.appendChild(cancel);
    row.appendChild(action);
    waitingBody.appendChild(row);
  });

  data.treated.forEach(p => {
    const row = document.createElement('tr');
    [p.patient_id, p.name, p.emergency_level, p.arrival_time].forEach(value => {
      const cell = document.createElement('td');
      cell.textContent = value;
      row.appendChild(cell);
    });
    treatedBody.appendChild(row);
  });
}

async function showMessage(response) {
  const data = await response.json();
  message.textContent = data.message;
  await refreshLists();
}

document.getElementById('register-form').addEventListener('submit', async event => {
  event.preventDefault();
  const response = await fetch('/api/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      patient_id: document.getElementById('patient-id').value,
      name: document.getElementById('patient-name').value,
      emergency_level: document.getElementById('emergency-level').value
    })
  });
  await showMessage(response);
  if (response.ok) event.target.reset();
});

document.getElementById('treat-button').addEventListener('click', async () => {
  await showMessage(await fetch('/api/treat', {method: 'POST'}));
});

document.getElementById('search-form').addEventListener('submit', async event => {
  event.preventDefault();
  const id = document.getElementById('search-id').value;
  await showMessage(await fetch('/api/search?patient_id=' + encodeURIComponent(id)));
});

async function cancelPatient(id) {
  await showMessage(await fetch('/api/cancel/' + id, {method: 'DELETE'}));
}

refreshLists();
