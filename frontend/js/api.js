const API_BASE_URL = 'http://localhost:8000/api';
const AUTH_TOKEN_KEY = 'authToken';
const CURRENT_USER_KEY = 'currentUser';

// API Helper Functions
async function apiCall(endpoint, method = 'GET', data = null, authenticated = false) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (authenticated) {
        const token = localStorage.getItem(AUTH_TOKEN_KEY);
        if (token) {
            options.headers['Authorization'] = `Bearer ${token}`;
        }
    }

    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (response.status === 401) {
            // Token expired or invalid
            logout();
            window.location.href = 'login.html';
            return null;
        }

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Call Error:', error);
        showAlert('error', 'An error occurred. Please try again.');
        return null;
    }
}

// Authentication Functions
async function login(email, password) {
    const response = await apiCall('/auth/login/', 'POST', { email, password });
    if (response && response.token && response.user) {
        localStorage.setItem(AUTH_TOKEN_KEY, response.token);
        localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(response.user));
        updateAuthUI();
        return true;
    }
    return false;
}

async function register(userData) {
    const response = await apiCall('/auth/register/', 'POST', userData);
    if (response && response.token && response.user) {
        localStorage.setItem(AUTH_TOKEN_KEY, response.token);
        localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(response.user));
        updateAuthUI();
        return true;
    }
    return false;
}

function logout() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(CURRENT_USER_KEY);
    localStorage.removeItem('cart');
    updateAuthUI();
    window.location.href = 'index.html';
}

function isAuthenticated() {
    return !!localStorage.getItem(AUTH_TOKEN_KEY);
}

function getCurrentUser() {
    const user = localStorage.getItem(CURRENT_USER_KEY);
    return user ? JSON.parse(user) : null;
}

// UI Update Functions
function updateAuthUI() {
    const authButtons = document.querySelector('.auth-buttons');
    if (!authButtons) return;

    if (isAuthenticated()) {
        const user = getCurrentUser();
        authButtons.innerHTML = `
            <a href="profile.html" class="btn btn-outline">${user.first_name || user.username}</a>
            <button onclick="logout()" class="btn btn-primary">Logout</button>
        `;
    } else {
        authButtons.innerHTML = `
            <a href="login.html" class="btn btn-outline">Login</a>
            <a href="register.html" class="btn btn-primary">Sign Up</a>
        `;
    }
}

// Alert/Notification Functions
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; font-size: 1.2rem; cursor: pointer;">×</button>
    `;
    
    document.body.insertBefore(alertDiv, document.body.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Loading Functions
function showLoading(element) {
    element.innerHTML = '<div class="spinner"></div>';
}

function hideLoading(element) {
    element.innerHTML = '';
}

// Cart Functions
function getCart() {
    const cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : { items: [], total: 0 };
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(item) {
    let cart = getCart();
    const existingItem = cart.items.find(i => i.id === item.id);
    
    if (existingItem) {
        existingItem.quantity += item.quantity || 1;
    } else {
        cart.items.push({
            ...item,
            quantity: item.quantity || 1
        });
    }
    
    updateCartTotal(cart);
    saveCart(cart);
    showAlert('success', `${item.name} added to cart!`);
}

function removeFromCart(itemId) {
    let cart = getCart();
    cart.items = cart.items.filter(i => i.id !== itemId);
    updateCartTotal(cart);
    saveCart(cart);
}

function updateCartItemQuantity(itemId, quantity) {
    let cart = getCart();
    const item = cart.items.find(i => i.id === itemId);
    if (item) {
        if (quantity <= 0) {
            removeFromCart(itemId);
        } else {
            item.quantity = quantity;
            updateCartTotal(cart);
            saveCart(cart);
        }
    }
}

function updateCartTotal(cart) {
    cart.total = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

// Format Functions
function formatPrice(price) {
    return new Intl.NumberFormat('en-GH', {
        style: 'currency',
        currency: 'GHS'
    }).format(price);
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Menu Item Functions
async function loadMenuItems(categoryId = null) {
    const endpoint = categoryId ? `/menu/items/?category=${categoryId}` : '/menu/items/';
    const data = await apiCall(endpoint);
    return data ? data.results || data : [];
}

async function loadCategories() {
    const data = await apiCall('/menu/categories/');
    return data ? data.results || data : [];
}

// Order Functions
async function createOrder(orderData) {
    const response = await apiCall('/orders/', 'POST', orderData, true);
    return response;
}

async function getOrders() {
    const data = await apiCall('/orders/', 'GET', null, true);
    return data ? (data.results || data) : [];
}

async function getOrderDetail(orderId) {
    const data = await apiCall(`/orders/${orderId}/`, 'GET', null, true);
    return data;
}

// Reservation Functions
async function createReservation(reservationData) {
    const response = await apiCall('/reservations/', 'POST', reservationData, true);
    return response;
}

async function getReservations() {
    const data = await apiCall('/reservations/', 'GET', null, true);
    return data ? (data.results || data) : [];
}

// Contact Functions
async function sendContactMessage(messageData) {
    const response = await apiCall('/contact/', 'POST', messageData);
    return response;
}

// Validation Functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^\d{10,}$/;
    return re.test(phone.replace(/[^\d]/g, ''));
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
});
