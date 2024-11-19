import { apiCall, createElement } from './utils.js';

async function fetchItems() {
    const pantryList = document.getElementById('pantry-list');
    pantryList.innerHTML = ''; // Clear the list

    try {
        const items = await apiCall(API_URL); // Fetch items using the global API_URL
        items.forEach(item => {
            const li = createElement('li', { 'data-id': item.id }, `${item.name} (${item.quantity})`);

            const deleteButton = createElement('button', {}, 'Delete');
            deleteButton.onclick = () => deleteItem(item.id);

            li.appendChild(deleteButton);
            pantryList.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching pantry items:", error);
    }
}

async function addItem() {
    const name = document.getElementById('item-name').value;
    const quantity = document.getElementById('item-quantity').value;

    if (name && quantity) {
        try {
            await apiCall(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, quantity: parseInt(quantity) }),
            });
            fetchItems();
        } catch (error) {
            console.error("Error adding item:", error);
        }
    } else {
        console.warn("Name or quantity is missing");
    }
}

async function deleteItem(id) {
    try {
        await apiCall(`${API_URL}/${id}`, { method: 'DELETE' });
        fetchItems();
    } catch (error) {
        console.error("Error deleting item:", error);
    }
}

export { fetchItems, addItem, deleteItem };
