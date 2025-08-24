// API Configuration
// Automatically detects environment and uses appropriate API URL

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default API_BASE_URL;

// Export for different use cases
export const getApiUrl = (endpoint = '') => {
    const baseUrl = API_BASE_URL.endsWith('/') ? API_BASE_URL.slice(0, -1) : API_BASE_URL;
    const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${baseUrl}${path}`;
};

// For axios instances
export const createApiConfig = () => ({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});