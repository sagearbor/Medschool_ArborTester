import { useState } from 'react';
import axios from 'axios';
import { getApiUrl } from '../config/api';

export default function SsoLogin() {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        try {
            const response = await axios.post(getApiUrl('/api/v1/auth/sso/login'), { email });
            setMessage(response.data.message);
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred.');
        }
    };

    return (
        <div>
            <h1>Institutional Sign In</h1>
            <p>Enter your institutional email address to begin.</p>
            <form onSubmit={handleSubmit}>
                <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="user@university.edu" required />
                <button type="submit">Continue</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {message && <p style={{ color: 'green' }}>{message}</p>}
        </div>
    );
}