import { apiCall, createElement } from './utils.js';

const PREVIEW_API_URL = "/pantry/preview-items";
const SAVE_API_URL = "/pantry/save-items";

/**
 * Adds a new row for entering item details.
 */
function addRow() {
    const row = createElement('div', { class: 'item-row' });
    row.innerHTML = `
        <input type="text" name="name[]" placeholder="Item Name" required>
        <input type="number" name="quantity[]" placeholder="Quantity" required>
    `;
    document.getElementById('item-rows').appendChild(row);
}

/**
 * Fetches the preview of items to be added and displays them in a table.
 */
async function previewItems() {
    const formData = new FormData(document.getElementById('add-items-form'));
    try {
        const data = await apiCall(PREVIEW_API_URL, { method: 'POST', body: formData });
        displayPreview(data.preview); // Call displayPreview with fetched items
    } catch (error) {
        console.error("Failed to preview items:", error);
    }
}

/**
 * Displays the previewed items in the preview section.
 * @param {Array} items - Array of items with `name` and `quantity`.
 */
function displayPreview(items) {
    const previewSection = document.getElementById('preview-section');
    const previewTable = document.getElementById('preview-table').querySelector('tbody');
    previewTable.innerHTML = ''; // Clear previous rows

    items.forEach(item => {
        const row = createElement('tr');
        row.innerHTML = `<td>${item.name}</td><td>${item.quantity}</td>`;
        previewTable.appendChild(row);
    });

    previewSection.style.display = 'block'; // Show the preview section
}

/**
 * Confirms and saves the previewed items to the backend.
 */
async function confirmAndSave() {
    const previewTable = document.getElementById('preview-table');
    const rows = Array.from(previewTable.querySelectorAll('tr'));
    
    // Map rows to items, ensuring valid structure
    const items = rows
        .map(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length === 2) { // Ensure both name and quantity cells exist
                return { 
                    name: cells[0].textContent.trim(), 
                    quantity: parseInt(cells[1].textContent.trim()) 
                };
            }
            return null; // Ignore invalid rows
        })
        .filter(item => item !== null); // Remove null values

    if (items.length === 0) {
        console.error("No valid items found to save.");
        alert("No valid items to save.");
        return;
    }

    try {
        const response = await apiCall(SAVE_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items }),
        });
        alert("Items saved successfully!");
        window.location.reload(); // Reload the page to reset the form
    } catch (error) {
        console.error("Failed to save items:", error);
        alert("Failed to save items. Please try again.");
    }
}

// Exporting functions for use in main.js
export { addRow, previewItems, confirmAndSave };
