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
    const [apiClient, setApiClient] = useState(null);
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [userAnswer, setUserAnswer] = useState('');
    const [feedback, setFeedback] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        setApiClient(createApiClient(token));
    }, [token]);

    useEffect(() => {
        if (apiClient) {
            fetchQuestion();
        }
    }, [apiClient]);

    const handleApiError = (err) => {
        if (err.response?.status === 401) {
            setError("Authentication failed. Please log in again.");
        } else {
            setError(err.response?.data?.detail || "An unexpected error occurred.");
        }
    };

    const fetchQuestion = async () => {
        if (!apiClient) return;
        try {
            const response = await apiClient.get('/api/v1/chat/question');
            setCurrentQuestion(response.data);
            setFeedback('');
            setError('');
        } catch (err) {
            handleApiError(err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!currentQuestion || !apiClient) return;

        try {
            const response = await apiClient.post('/api/v1/chat/answer', {
                question_id: currentQuestion.id,
                user_answer: userAnswer,
            });
            setFeedback(`Your answer was ${response.data.is_correct ? 'correct' : 'incorrect'}.`);
            setUserAnswer('');
        } catch (err) {
            handleApiError(err);
        }
    };

    return (
        <div>
            {currentQuestion ? (
                <div>
                    <h3>Question:</h3>
                    <p>{currentQuestion.content}</p>
                </div>
            ) : (
                <p>Loading question...</p>
            )}

            <form onSubmit={handleSubmit}>
                <textarea
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                    rows="4"
                    cols="50"
                />
                <br />
                <button type="submit">Submit Answer</button>
            </form>

            {feedback && <p><strong>Feedback:</strong> {feedback}</p>}
            {error && <p style={{ color: 'red' }}><strong>Error:</strong> {error}</p>}

            <button onClick={fetchQuestion}>Next Question</button>
        </div>
    );
}