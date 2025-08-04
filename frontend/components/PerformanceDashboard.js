import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function PerformanceDashboard({ data }) {
    const chartData = data.map(item => ({
        ...item,
        accuracy: (item.accuracy * 100).toFixed(1),
    }));

    return (
        <div style={{ width: '100%', height: 400 }}>
            <h3>Accuracy by Discipline</h3>
            <ResponsiveContainer>
                <BarChart
                    data={chartData}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="discipline" />
                    <YAxis unit="%" domain={[0, 100]} />
                    <Tooltip formatter={(value) => `${value}%`} />
                    <Legend />
                    <Bar dataKey="accuracy" fill="#8884d8" name="Correct Answers (%)" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}