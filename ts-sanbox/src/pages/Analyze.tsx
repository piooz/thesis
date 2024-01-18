import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import FileUpload from '../components/FileUpload';
import ResultChart from '../components/ResultChart';
import {data} from '../mock/analysis-result'


const Analyze = () => {
    console.log(data)

    return (
        <div>
            <ResultChart data={data}/>
        </div>
    );
}

export default Analyze;
