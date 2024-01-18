import { CartesianGrid, ComposedChart, Legend, Line, Scatter, Tooltip, XAxis, YAxis } from "recharts";


const ResultChart = (data: any) => {
    return (
            <ComposedChart
                width={1000}
                height={700}
                data={data.data}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="index"/>
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dot={false} dataKey="output" stroke="#8884d8"  />
                <Line type="monotone" dot={false} dataKey="origin" stroke="#82ca9d" strokeDasharray="3 4 5 2" />
                <Scatter name="TC" dataKey="TC" fill="blue"/>
                <Scatter name="IO" dataKey="IO" fill="red"/>
                <Scatter name="LS" dataKey="LS" fill="orange"/>
                <Scatter name="AO" dataKey="AO" fill="green"/>
            </ComposedChart>
    );
}
export default ResultChart;
