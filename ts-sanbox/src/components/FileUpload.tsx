import React, { useState } from 'react';
import axios from 'axios';
import CSVReader from 'react-csv-reader';
import ResultChart from './ResultChart';
import {data} from '../mock/analysis-result'


const FileUpload = () => {
    const [fileData, setFileData] = useState(null);

    const handleFileUpload = (data:any) => {
        console.log(data)
        if (data.length === 0 || data[0].length !== 1) {
            console.error('Invalid CSV format. Please upload a non-empty CSV file with one column (without heading).');
            return;
        }

        const nonEmptyData = data.filter((row:any) => row.length > 0);
        const csvData = nonEmptyData.map((row:any) => row[0]);

        setFileData(data);
        // sendToBackend(csvData);
    };

    const sendToBackend = async (data:any) => {
        try {
            const formData = new FormData();
            formData.append('csvFile', new Blob([data.join('\n')], { type: 'text/csv' }), 'filename.csv');

            const response = await axios.post('your-backend-api-endpoint', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log('Backend response:', response.data);
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };

    console.log(data)

    return (
        <div>
            <h1>CSV File Upload (One Column)</h1>
            <CSVReader onFileLoaded={handleFileUpload} />
            {fileData && (
                <div>
                    <ResultChart data={data}/>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
