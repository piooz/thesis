import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import {data2} from "../mock/analysis-result"


const Effects = () => {
    return (
        <>
        <h1>Generate Effect</h1>
            <LineChart
                width={1000}
                height={700}
                data={data2}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis/>
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dot={false} dataKey="uv" stroke="#8884d8"  />
                <Line type="monotone" dot={false} dataKey="pv" stroke="#82ca9d" strokeDasharray="3 4 5 2" />
            </LineChart>
        </>
    );
}

export default Effects
