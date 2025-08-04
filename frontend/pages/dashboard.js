import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import axios from 'axios';
import PerformanceDashboard from '../components/PerformanceDashboard';

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
        <div>
            <h1>Performance Dashboard</h1>
            <nav style={{ marginBottom: '20px' }}>
                <Link href="/dashboard" style={{ marginRight: '10px' }}>Live Data</Link> | 
                <Link href="/dashboard?useTestData=true" style={{ marginLeft: '10px' }}>Demo Data</Link>
            </nav>
            
            {isLoading && <p>Loading dashboard...</p>}
            {error && <p style={{ color: 'red' }}>Error: {error}</p>}
            
            {!isLoading && !error && analyticsData && (
                <PerformanceDashboard data={analyticsData} />
            )}
            {!isLoading && !error && !analyticsData && (
                <p>No performance data available yet.</p>
            )}
        </div>
    );
}