const API_URL = "{{ api_url }}";  // This is the dynamic API URL passed by Flask
console.log("Using API URL:", API_URL);

async function fetchItems() {
    const response = await fetch(API_URL);
    const items = await response.json();
    const pantryList = document.getElementById('pantry-list');
    pantryList.innerHTML = ''; // Clear the list
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} (${item.quantity})`;
        li.dataset.id = item.id;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deleteItem(item.id);

        li.appendChild(deleteButton);
        pantryList.appendChild(li);
    });
}

async function addItem() {
    const name = document.getElementById('item-name').value;
    const quantity = document.getElementById('item-quantity').value;

    if (name && quantity) {
        await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, quantity: parseInt(quantity) }),
        });
        fetchItems();
    }
}

async function deleteItem(id) {
    await fetch(`${API_URL}/${id}`, {
        method: 'DELETE',
    });
    fetchItems();
}

document.getElementById('add-button').addEventListener('click', addItem);
fetchItems();
