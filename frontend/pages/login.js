import { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await axios.post('http://localhost:8000/api/v1/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });
            
            localStorage.setItem('authToken', response.data.access_token);
            router.push('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred.');
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" required />
                <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" required />
                <button type="submit">Login</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            <hr />
            <a href="http://localhost:8000/api/v1/auth/google/login">
                <button>Sign in with Google</button>
            </a>
        </div>
    );
}