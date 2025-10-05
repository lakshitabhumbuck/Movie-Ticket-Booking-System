// Simple JavaScript for Movie Booking System
// Minimal functionality - mostly handled in templates

// Basic utility functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main .container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('access_token') !== null;
}

// Get auth headers for API calls
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
}

// Simple logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.reload();
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    updateAuthUI();
});

// Update authentication UI
function updateAuthUI() {
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (token && user.username) {
        document.getElementById('auth-buttons').classList.add('d-none');
        document.getElementById('user-menu').classList.remove('d-none');
        document.getElementById('username-display').textContent = user.username;
    } else {
        document.getElementById('auth-buttons').classList.remove('d-none');
        document.getElementById('user-menu').classList.add('d-none');
    }
}
