// static/js/auth.js
class Auth {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.checkAuth();
    }

    checkAuth() {
        // Redirect to login if no token (except on login page)
        if (!this.token && !window.location.pathname.includes('/login')) {
            window.location.href = '/login';
        }
    }

    async login(loginFormData) {
        try {
            const response = await fetch('/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: loginFormData,
            });

            if (!response.ok) throw new Error('Login failed');

            const data = await response.json();
            this.token = data.access_token;
            localStorage.setItem('access_token', this.token);
            window.location.href = '/dashboard';
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async fetchWithAuth(url, options = {}) {
        if (!this.token) {
            window.location.href = '/login';
            return;
        }

        const response = await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${this.token}`
            }
        });

        if (response.status === 401) {
            this.logout();
            return;
        }

        return response;
    }

    logout() {
        this.token = null;
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    }
}

// Initialize auth globally
window.auth = new Auth();