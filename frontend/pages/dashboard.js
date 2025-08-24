import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import axios from 'axios';
import PerformanceDashboard from '../components/PerformanceDashboard';
import Navigation from '../components/Navigation';
import { createApiConfig } from '../config/api';

const createApiClient = (token) => {
    const apiClient = axios.create(createApiConfig());
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
    const [groupBy, setGroupBy] = useState('disciplines');
    const router = useRouter();

    const taxonomyOptions = [
        { value: 'disciplines', label: 'Medical Disciplines', description: 'Anatomy, Pharmacology, Pathology, etc.' },
        { value: 'body_systems', label: 'Body Systems', description: 'Cardiovascular, Respiratory, Neurological, etc.' },
        { value: 'specialties', label: 'Medical Specialties', description: 'Internal Medicine, Surgery, Pediatrics, etc.' },
        { value: 'question_type', label: 'Question Types', description: 'Diagnosis, Treatment, Mechanism, etc.' },
        { value: 'age_group', label: 'Age Groups', description: 'Adult, Child, Elderly, etc.' },
        { value: 'acuity', label: 'Acuity Levels', description: 'Life-threatening, Urgent, Routine, etc.' },
        { value: 'pathophysiology', label: 'Pathophysiology', description: 'Infectious, Autoimmune, Neoplastic, etc.' }
    ];

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        const { useTestData } = router.query;

        if (!token && !useTestData) {
            setError("No token found. Please log in.");
            setIsLoading(false);
            return;
        }

        const apiClient = createApiClient(token);

        const fetchAnalytics = async (selectedGroupBy = groupBy) => {
            setIsLoading(true);
            try {
                const params = new URLSearchParams();
                if (useTestData) params.append('useTestData', 'true');
                params.append('group_by', selectedGroupBy);
                
                const url = `/api/v1/analytics/summary?${params.toString()}`;
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
    }, [router.query, groupBy]);

    const handleGroupByChange = (newGroupBy) => {
        setGroupBy(newGroupBy);
    };

    return (
        <div className="min-h-screen bg-gray-50">
            <Navigation />
            
            <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                <div className="mb-6">
                    <h1 className="text-3xl font-bold text-gray-900">Performance Dashboard</h1>
                    <p className="mt-1 text-sm text-gray-600">Track your learning progress and performance metrics</p>
                </div>

                {/* Controls */}
                <div className="mb-6 bg-white rounded-lg shadow p-4">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
                        {/* Data Toggle */}
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

                        {/* Taxonomy Selector */}
                        <div className="flex items-center space-x-3">
                            <label htmlFor="groupBy" className="text-sm font-medium text-gray-700">
                                Group by:
                            </label>
                            <select
                                id="groupBy"
                                value={groupBy}
                                onChange={(e) => handleGroupByChange(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            >
                                {taxonomyOptions.map((option) => (
                                    <option key={option.value} value={option.value} title={option.description}>
                                        {option.label}
                                    </option>
                                ))}
                            </select>
                        </div>
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