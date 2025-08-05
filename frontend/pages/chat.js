import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import ChatWindow from '../components/ChatWindow';
import Navigation from '../components/Navigation';

export default function ChatPage() {
    const [token, setToken] = useState(null);
    const [isClient, setIsClient] = useState(false);
    const router = useRouter();

    useEffect(() => {
        setIsClient(true);
        const storedToken = localStorage.getItem('authToken');
        if (storedToken) {
            setToken(storedToken);
        } else {
            router.push('/login');
        }
    }, [router]);

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        router.push('/login');
    };

    if (!isClient) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!token) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <h1 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h1>
                    <p className="text-gray-600 mb-6">Please log in to access the AI tutor</p>
                    <Link href="/login" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-200">
                        Go to Login
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />

            {/* Main Content */}
            <main className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
                <div className="bg-white rounded-xl shadow-lg overflow-hidden">
                    <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4">
                        <h2 className="text-xl font-semibold text-white">AI-Powered Clinical Questions</h2>
                        <p className="text-blue-100 text-sm mt-1">Practice with real medical board exam scenarios</p>
                    </div>
                    <div className="p-6">
                        <ChatWindow token={token} />
                    </div>
                </div>
            </main>
        </div>
    );
}