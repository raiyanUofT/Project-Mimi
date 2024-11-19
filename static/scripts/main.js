import { fetchItems, addItem, deleteItem } from './pantry.js';
import { addRow, previewItems, confirmAndSave } from './add_items.js';

document.addEventListener('DOMContentLoaded', () => {
    const page = document.body.dataset.page;

    if (page === 'pantry') {
        const addButton = document.getElementById('add-button');
        if (addButton) {
            addButton.addEventListener('click', addItem);
        }
        fetchItems();
    } else if (page === 'add-items') {
        const addRowButton = document.getElementById('add-row-button');
        const previewButton = document.getElementById('preview-button');
        const confirmButton = document.getElementById('confirm-button');

        if (addRowButton) {
            addRowButton.addEventListener('click', addRow);
        }
        if (previewButton) {
            previewButton.addEventListener('click', previewItems);
        }
        if (confirmButton) {
            confirmButton.addEventListener('click', confirmAndSave);
        }
    }
});
