import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function PerformanceDashboard({ data }) {
    const chartData = data.map(item => ({
        ...item,
        correct_answers: item.correct_count,
        incorrect_answers: item.total_answered - item.correct_count,
        accuracy_percent: (item.accuracy * 100).toFixed(1)
    }));

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
                    <p className="font-semibold text-gray-800">{`${label}`}</p>
                    <p className="text-green-600">
                        <span className="inline-block w-3 h-3 bg-green-500 mr-2"></span>
                        {`Correct: ${data.correct_answers}`}
                    </p>
                    <p className="text-red-600">
                        <span className="inline-block w-3 h-3 bg-red-500 mr-2"></span>
                        {`Incorrect: ${data.incorrect_answers}`}
                    </p>
                    <p className="text-gray-600 mt-1 pt-1 border-t">
                        {`Total: ${data.total_answered} (${data.accuracy_percent}% correct)`}
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h3>
            <div style={{ width: '100%', height: 400 }}>
                <ResponsiveContainer>
                    <BarChart
                        data={chartData}
                        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                        <XAxis 
                            dataKey="discipline" 
                            tick={{ fontSize: 12 }}
                            angle={-45}
                            textAnchor="end"
                            height={80}
                        />
                        <YAxis 
                            label={{ value: 'Number of Questions', angle: -90, position: 'insideLeft' }}
                            tick={{ fontSize: 12 }}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Bar 
                            dataKey="correct_answers" 
                            stackId="a" 
                            fill="#10b981" 
                            name="Correct Answers"
                            radius={[0, 0, 0, 0]}
                        />
                        <Bar 
                            dataKey="incorrect_answers" 
                            stackId="a" 
                            fill="#ef4444" 
                            name="Incorrect Answers"
                            radius={[4, 4, 0, 0]}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}