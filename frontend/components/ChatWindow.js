import { useState, useEffect } from 'react';
import axios from 'axios';

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

export default function ChatWindow({ token }) {
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [userAnswer, setUserAnswer] = useState('');
    const [feedback, setFeedback] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [specialty, setSpecialty] = useState('General Medicine');
    const [difficulty, setDifficulty] = useState('Intermediate');
    const [customTopic, setCustomTopic] = useState('');


    const handleApiError = (err) => {
        console.error('API Error:', err);
        if (err.response?.status === 401) {
            // Clear invalid token
            localStorage.removeItem('authToken');
            
            // Show prominent error message
            setError("🔒 Your session has expired. Redirecting to login page...");
            
            // Redirect to login after 2 seconds
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            setError(err.response?.data?.detail || "An unexpected error occurred.");
        }
        setLoading(false);
    };

    const fetchQuestion = async (requestedTopic = '') => {
        if (!token) return;
        setLoading(true);
        setError('');
        
        const client = createApiClient(token);
        
        try {
            let url = '/api/v1/chat/question';
            const params = new URLSearchParams();
            
            if (requestedTopic) {
                params.append('specialty', requestedTopic);
            } else {
                params.append('specialty', specialty);
            }
            params.append('difficulty', difficulty);
            
            if (params.toString()) {
                url += '?' + params.toString();
            }
            
            console.log('Fetching question from:', url);
            const response = await client.get(url);
            setCurrentQuestion(response.data);
            setFeedback('');
            setError('');
        } catch (err) {
            handleApiError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!currentQuestion || !token || !userAnswer.trim()) return;

        const client = createApiClient(token);
        setLoading(true);
        try {
            const response = await client.post('/api/v1/chat/answer', {
                question_id: currentQuestion.id,
                user_answer: userAnswer,
            });
            
            const result = response.data;
            setFeedback({
                isCorrect: result.is_correct,
                correctAnswer: result.correct_answer,
                explanation: result.explanation,
                personalizedFeedback: result.personalized_feedback
            });
            setUserAnswer('');
        } catch (err) {
            handleApiError(err);
        } finally {
            setLoading(false);
        }
    };

    const handleCustomTopicSubmit = (e) => {
        e.preventDefault();
        if (customTopic.trim()) {
            fetchQuestion(customTopic.trim());
            setCustomTopic('');
        }
    };

    const parseQuestionOptions = (question) => {
        if (!question || !question.options) return null;
        
        try {
            const options = typeof question.options === 'string' 
                ? JSON.parse(question.options) 
                : question.options;
            return options;
        } catch (e) {
            console.error('Error parsing options:', e);
            return null;
        }
    };

    const questionOptions = currentQuestion ? parseQuestionOptions(currentQuestion) : null;

    return (
        <div className="space-y-6">
            {/* Topic Request Section */}
            <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-blue-900 mb-3">Request a Question</h3>
                
                {/* Quick Presets */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-4">
                    <button
                        onClick={() => fetchQuestion('Cardiology')}
                        disabled={loading}
                        className="px-3 py-2 bg-white border border-blue-200 rounded-md hover:bg-blue-50 text-sm font-medium transition duration-200 disabled:opacity-50"
                    >
                        Cardiology
                    </button>
                    <button
                        onClick={() => fetchQuestion('Neurology')}
                        disabled={loading}
                        className="px-3 py-2 bg-white border border-blue-200 rounded-md hover:bg-blue-50 text-sm font-medium transition duration-200 disabled:opacity-50"
                    >
                        Neurology
                    </button>
                    <button
                        onClick={() => fetchQuestion('Emergency Medicine')}
                        disabled={loading}
                        className="px-3 py-2 bg-white border border-blue-200 rounded-md hover:bg-blue-50 text-sm font-medium transition duration-200 disabled:opacity-50"
                    >
                        Emergency
                    </button>
                    <button
                        onClick={() => fetchQuestion('Pediatrics')}
                        disabled={loading}
                        className="px-3 py-2 bg-white border border-blue-200 rounded-md hover:bg-blue-50 text-sm font-medium transition duration-200 disabled:opacity-50"
                    >
                        Pediatrics
                    </button>
                    <button
                        onClick={() => fetchQuestion('Surgery')}
                        disabled={loading}
                        className="px-3 py-2 bg-white border border-blue-200 rounded-md hover:bg-blue-50 text-sm font-medium transition duration-200 disabled:opacity-50"
                    >
                        Surgery
                    </button>
                    <button
                        onClick={() => fetchQuestion('Internal Medicine')}
                        disabled={loading}
                        className="px-3 py-2 bg-white border border-blue-200 rounded-md hover:bg-blue-50 text-sm font-medium transition duration-200 disabled:opacity-50"
                    >
                        Internal Med
                    </button>
                </div>

                {/* Custom Topic */}
                <form onSubmit={handleCustomTopicSubmit} className="flex gap-2">
                    <input
                        type="text"
                        value={customTopic}
                        onChange={(e) => setCustomTopic(e.target.value)}
                        placeholder="Or enter any medical topic..."
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        disabled={loading || !customTopic.trim()}
                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
                    >
                        Generate Question
                    </button>
                </form>
            </div>

            {/* Question Display */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
                {loading ? (
                    <div className="text-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                        <p className="text-gray-600">Generating your medical question...</p>
                    </div>
                ) : currentQuestion ? (
                    <div className="space-y-4">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-3">Clinical Question</h3>
                            <p className="text-gray-800 leading-relaxed">{currentQuestion.content}</p>
                        </div>

                        {/* Multiple Choice Options */}
                        {questionOptions && (
                            <div className="space-y-2">
                                <h4 className="font-medium text-gray-900">Choose the best answer:</h4>
                                <div className="space-y-1">
                                    {Object.entries(questionOptions).map(([key, value]) => (
                                        <label key={key} className="flex items-start space-x-2 cursor-pointer p-2 rounded hover:bg-gray-50">
                                            <input
                                                type="radio"
                                                name="mcq_answer"
                                                value={key}
                                                checked={userAnswer === key}
                                                onChange={(e) => setUserAnswer(e.target.value)}
                                                className="mt-1"
                                            />
                                            <span className="text-sm"><strong>{key}.</strong> {value}</span>
                                        </label>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Submit Button */}
                        <button
                            onClick={handleSubmit}
                            disabled={loading || !userAnswer}
                            className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Submitting...' : 'Submit Answer'}
                        </button>
                    </div>
                ) : (
                    <div className="text-center py-8">
                        <p className="text-gray-600 mb-4">Click a topic above or enter a custom topic to generate your first question!</p>
                        <button
                            onClick={() => fetchQuestion()}
                            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-200"
                        >
                            Generate Random Question
                        </button>
                    </div>
                )}
            </div>

            {/* Feedback Section */}
            {feedback && (
                <div className={`rounded-lg p-4 ${feedback.isCorrect ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                    <div className="flex items-start space-x-2">
                        <div className={`w-5 h-5 rounded-full flex items-center justify-center text-white text-xs font-bold ${feedback.isCorrect ? 'bg-green-500' : 'bg-red-500'}`}>
                            {feedback.isCorrect ? '✓' : '✗'}
                        </div>
                        <div className="flex-1">
                            <p className={`font-medium ${feedback.isCorrect ? 'text-green-800' : 'text-red-800'}`}>
                                {feedback.isCorrect ? 'Correct!' : 'Incorrect'}
                            </p>
                            {!feedback.isCorrect && (
                                <p className="text-sm text-gray-700 mt-1">
                                    <strong>Correct answer:</strong> {feedback.correctAnswer}
                                </p>
                            )}
                            {feedback.explanation && (
                                <p className="text-sm text-gray-700 mt-2">
                                    <strong>Explanation:</strong> {feedback.explanation}
                                </p>
                            )}
                            {feedback.personalizedFeedback && (
                                <p className="text-sm text-gray-700 mt-2">
                                    <strong>AI Feedback:</strong> {feedback.personalizedFeedback}
                                </p>
                            )}
                        </div>
                    </div>
                    
                    <button
                        onClick={() => fetchQuestion()}
                        disabled={loading}
                        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-200 disabled:opacity-50"
                    >
                        Next Question
                    </button>
                </div>
            )}

            {/* Error Display */}
            {error && (
                <div className={`rounded-lg p-4 ${error.includes('🔒') ? 'bg-yellow-100 border-2 border-yellow-400' : 'bg-red-50 border border-red-200'}`}>
                    <p className={`${error.includes('🔒') ? 'text-yellow-800 text-lg font-semibold' : 'text-red-600'}`}>
                        <strong>{error.includes('🔒') ? '' : 'Error: '}</strong>{error}
                    </p>
                    {!error.includes('🔒') && (
                        <button
                            onClick={() => fetchQuestion()}
                            className="mt-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition duration-200"
                        >
                            Try Again
                        </button>
                    )}
                </div>
            )}
        </div>
    );
}