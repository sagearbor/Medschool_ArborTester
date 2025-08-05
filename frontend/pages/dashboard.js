import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import axios from 'axios';
import PerformanceDashboard from '../components/PerformanceDashboard';
import Navigation from '../components/Navigation';

const createApiClient = (token) => {
    const apiClient = axios.create({
        baseURL: 'http://localhost:8000',
    });
    apiClient.interceptors.request.use((config) => {
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    });
    return apiClient;
};

export default function DashboardPage() {
    const [analyticsData, setAnalyticsData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        const { useTestData } = router.query;

        if (!token && !useTestData) {
            setError("No token found. Please log in.");
            setIsLoading(false);
            return;
        }

        const apiClient = createApiClient(token);

        const fetchAnalytics = async () => {
            setIsLoading(true);
            try {
                const url = `/api/v1/analytics/summary${useTestData ? '?useTestData=true' : ''}`;
                const response = await apiClient.get(url);
                setAnalyticsData(response.data.performance_by_discipline);
            } catch (err) {
                if (err.response?.status === 401) {
                    setError("Authentication failed. Please log in again.");
                } else {
                    setError("Could not fetch analytics data.");
                }
            } finally {
                setIsLoading(false);
            }
        };

        fetchAnalytics();
    }, [router.query]);

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />
            
            <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                <div className="mb-6">
                    <h1 className="text-3xl font-bold text-gray-900">Performance Dashboard</h1>
                    <p className="mt-1 text-sm text-gray-600">Track your learning progress and performance metrics</p>
                </div>

                {/* Data Toggle */}
                <div className="mb-6 bg-white rounded-lg shadow p-4">
                    <div className="flex space-x-4">
                        <Link 
                            href="/dashboard" 
                            className={`px-4 py-2 rounded-md text-sm font-medium transition duration-200 ${
                                !router.query.useTestData ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }`}
                        >
                            Live Data
                        </Link>
                        <Link 
                            href="/dashboard?useTestData=true" 
                            className={`px-4 py-2 rounded-md text-sm font-medium transition duration-200 ${
                                router.query.useTestData ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                            }`}
                        >
                            Demo Data
                        </Link>
                    </div>
                </div>
                
                {isLoading && (
                    <div className="bg-white rounded-lg shadow p-8 text-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                        <p className="text-gray-600">Loading dashboard...</p>
                    </div>
                )}
                
                {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                        <p className="text-red-600">Error: {error}</p>
                    </div>
                )}
                
                {!isLoading && !error && analyticsData && (
                    <PerformanceDashboard data={analyticsData} />
                )}
                
                {!isLoading && !error && !analyticsData && (
                    <div className="bg-white rounded-lg shadow p-8 text-center">
                        <p className="text-gray-600">No performance data available yet. Start practicing to see your progress!</p>
                        <Link href="/chat" className="mt-4 inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-200">
                            Start Practice
                        </Link>
                    </div>
                )}
            </main>
        </div>
    );
}