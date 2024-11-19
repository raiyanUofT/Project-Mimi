console.log("API URL in script.js:", API_URL);  // Debugging info

async function fetchItems() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Failed to fetch items");
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
    } catch (error) {
        console.error(error);
        alert("Failed to fetch pantry items");
    }
}

async function addItem() {
    const name = document.getElementById('item-name').value;
    const quantity = document.getElementById('item-quantity').value;

    if (name && quantity) {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, quantity: parseInt(quantity) }),
            });
            if (!response.ok) throw new Error("Failed to add item");
            fetchItems();  // Refresh the list
        } catch (error) {
            console.error(error);
            alert("Failed to add item");
        }
    }
}

async function deleteItem(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) throw new Error("Failed to delete item");
        fetchItems();  // Refresh the list
    } catch (error) {
        console.error(error);
        alert("Failed to delete item");
    }
}

document.getElementById('add-button').addEventListener('click', addItem);
fetchItems();  // Initial fetch
