import { Button } from '@mui/material';
import React from 'react';
import { Link } from 'react-router-dom';


export default function Home() {
    return (
        <>
            <h1 id="chen-liu-algorithm">Chen-Liu algorithm</h1>
            <p>This page is created to present, visualize, explain and try out chen-liu algorithm.</p>
            <h1 id="what-is-chen-liu-algorithm">What is Chen-Liu algorithm</h1>
            <p>The Chen-Liu algorithm is a statistical method for detecting outliers in time series data. It was developed by Chen and Liu in 1993 and is based on the concept of residual redundancy.</p>
            <p><a href="http://www.jstor.org/stable/2290724">Link to original article</a></p>
            <blockquote>
                <p>The Main goal is to design a procedure that is less
                    vulnerable to the spurious and masking effects during outlier detection and is able to jointly estimate the model parameters and outlier effect</p>
            </blockquote>
            <Button component={Link} to="./analyze">Analyze</Button>
        </>
    )
};
