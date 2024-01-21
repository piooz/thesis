import FileUpload from '../components/FileUpload';
import { data } from '../mock/analysis-result'


const Analyze = () => {
    console.log(data)

    return (
        <div>
            <FileUpload />
        </div>
    );
}

export default Analyze;
