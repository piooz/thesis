import React, { useState } from 'react';
import axios from 'axios';
import CSVReader from 'react-csv-reader';
import ResultChart from './ResultChart';
import { data } from '../mock/analysis-result'
import ResultTable from './ResultTable';
import Summary from './Summary';

const FileUpload = () => {
    const [outdata, setOutData] = useState(null);
    const [criticalValue, setCriticalValue] = useState("2");

    const handleFileUpload = (data: any) => {
        // if (data.length === 0 || data[0].length !== 1) {
        //     console.error('Invalid CSV format. Please upload a non-empty CSV file with one column (without heading).');
        //     return;
        // }
        //
        // const nonEmptyData = data.filter((row: any) => row.length > 0);
        // const csvData = nonEmptyData.map((row: any) => row[0]);
        //
        // sendToBackend(csvData);
    };

    const sendToBackend = async (data: any) => {
        try {
            const formData = new FormData();
            formData.append('csvFile', new Blob([data.join('\n')], { type: 'text/csv' }), 'filename.csv');
            formData.append('criticalValue', criticalValue);

            const response = await axios.post(`http://localhost:8000/test/?cval=${criticalValue}`, {formData});
            console.log('Backend response:', response.data);
            setOutData(response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    const handleCriticalValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setCriticalValue(event.target.value);
    };

    return (
        <div>
            <h1>CSV File Upload (One Column)</h1>
            <form>
                <label>
                    Critical Value:
                    <input type="text" value={criticalValue} onChange={handleCriticalValueChange} />
                </label>
                <br />
                <CSVReader onFileLoaded={handleFileUpload} />
                <button type="button" onClick={() => sendToBackend([])}>
                    Upload
                </button>
            </form>
            {outdata && (
                <div>
                    <ResultChart data={outdata.data} />
                    <Summary data={outdata} />
                    <h3>1st Stage calculated statistics</h3>
                    <ResultTable data={outdata.raport.stats} />
                </div>
            )}
        </div>
    );
};

export default FileUpload;
