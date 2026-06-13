import { useState } from "react";
import { uploadFile } from "../api/api";

function FileUpload() {

const [file, setFile] = useState(null);
const [message, setMessage] = useState("");
const [uploadedFiles, setUploadedFiles] = useState([]);
const [loading, setLoading] = useState(false);

const handleUpload = async () => {

    if (!file) return;

    setLoading(true);

    try {

        const response = await uploadFile(file);

        setMessage(response.data.message);

        setUploadedFiles(prev => {

            if (prev.includes(file.name))
                return prev;

            return [...prev, file.name];

        });

    } catch (error) {

        setMessage("Upload failed");
        console.log(error);

    } finally {

        setLoading(false);

    }
};

return (
    <div>

        <h2>Upload Document</h2>

        <div className="drop-zone">

            <input
                type="file"
                id="file-upload"
                hidden
                onChange={(e) => setFile(e.target.files[0])}
            />

            <label htmlFor="file-upload">

                {file
                    ? file.name
                    : "📄 Drag & Drop or Click to Upload"}

            </label>

        </div>

        <div className="upload-actions">

            <button
                onClick={handleUpload}
                disabled={loading}
            >
                {loading ? "Uploading..." : "Upload"}
            </button>

        </div>

        <p style={{ marginTop: "15px" }}>
            {message}
        </p>

        {uploadedFiles.length > 0 && (

            <div className="answer-box">

                <strong>
                    Indexed Documents ({uploadedFiles.length})
                </strong>

                <ul className="sources-list">

                    {uploadedFiles.map((fileName, index) => (

                        <li key={index}>
                            📄 {fileName}
                        </li>

                    ))}

                </ul>

            </div>

        )}

    </div>
);
}

export default FileUpload;
