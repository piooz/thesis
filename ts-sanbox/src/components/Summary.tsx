const Summary = (data: any) => {

    return (
        <>
            <h3>
                Summary:
            </h3>
            <p>
                Run: {data.data.id}
            </p>
            <p>
                Time: {data.data.time}
            </p>
            <p>
                Execution time: {data.data.raport.executionTime}
            </p>
            <h4>Arima model</h4>
            <h5>AR</h5>
            {
                data.data.raport.fit.arparams.map((n: any, i: any) =>
                    <p>
                        {i}: {n}
                    </p>
                )

            }
            <h5>MA</h5>
            {
                data.data.raport.fit.maparams.map((n: any, i: any) =>
                    <p>
                        {i}: {n}
                    </p>
                )
            }
        </>
    )

}

export default Summary
