// Fetch helper with error handling
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error(error);
        alert("Something went wrong. Please try again.");
        throw error; // Re-throw for specific handling if needed
    }
}

// DOM utility to create an element with attributes
function createElement(tag, attributes = {}, content = "") {
    const element = document.createElement(tag);
    Object.entries(attributes).forEach(([key, value]) => {
        element.setAttribute(key, value);
    });
    if (content) element.textContent = content;
    return element;
}

export { apiCall, createElement };
