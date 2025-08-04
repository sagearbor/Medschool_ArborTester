import { useEffect, useState } from 'react';
import ChatWindow from '../components/ChatWindow';

export default function ChatPage() {
    const [token, setToken] = useState(null);
    const [isClient, setIsClient] = useState(false);

    useEffect(() => {
        setIsClient(true);
        const storedToken = localStorage.getItem('authToken');
        if (storedToken) {
            setToken(storedToken);
        } else {
            console.log("No token found. Please log in.");
        }
    }, []);

    if (!isClient) {
        return null; // Don't render server-side
    }

    if (!token) {
        return <div>Please log in to use the chat.</div>;
    }

    return (
        <div>
            <h1>MedBoard AI Tutor</h1>
            <ChatWindow token={token} />
        </div>
    );
}