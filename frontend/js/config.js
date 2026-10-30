// Where the API lives. Locally the Flask app runs on port 5000; on AWS, Nginx forwards
// /api/* to the internal load balancer, so the browser only ever talks to its own origin.
const API_BASE = ["localhost", "127.0.0.1"].includes(window.location.hostname)
    ? "http://localhost:5000"
    : "/api";

// Anonymous cart owner: a random ID created once per browser (see backend/routes/common.py)
let memoryClientId = null;

function getClientId() {
    try {
        let id = localStorage.getItem("clientId");
        if (!id) {
            id = generateId();
            localStorage.setItem("clientId", id);
        }
        return id;
    } catch (error) {
        // localStorage blocked: keep the ID for this page session only
        memoryClientId = memoryClientId || generateId();
        return memoryClientId;
    }
}

function generateId() {
    const bytes = new Uint8Array(16);
    crypto.getRandomValues(bytes);
    return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

async function api(path, options = {}) {
    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "X-Client-Id": getClientId(),
            ...(options.headers || {}),
        },
    });

    let data = null;
    try {
        data = await response.json();
    } catch (error) {
        // non-JSON response; handled below
    }

    if (!response.ok) {
        throw new Error((data && data.message) || `Request failed (${response.status})`);
    }
    return data;
}

// Escape text before putting it into innerHTML
function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (c) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }[c]));
}

function formatPrice(amount) {
    return "₹" + Number(amount).toLocaleString("en-IN");
}
