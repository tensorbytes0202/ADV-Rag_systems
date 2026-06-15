import { useState } from "react";
import api from "../services/api";

function UploadSection() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const handleUpload = async () => {

        if (!file) {
            setMessage("Please select a PDF file");
            return;
        }

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        try {

            const response = await api.post(
                "/upload",
                formData,
                {
                    headers: {
                        "Content-Type":
                            "multipart/form-data",
                    },
                }
            );

            console.log(
                "SUCCESS RESPONSE:",
                response
            );

            console.log(
                "SUCCESS DATA:",
                response.data
            );

            setMessage(
                `✅ Uploaded Successfully | Chunks: ${response.data.total_chunks}`
            );

        } catch (error) {

            console.error(
                "UPLOAD ERROR:",
                error
            );

            console.error(
                "ERROR RESPONSE:",
                error.response
            );

            console.error(
                "ERROR DATA:",
                error.response?.data
            );

            setMessage(
                error.response?.data?.detail ||
                error.message ||
                "❌ Upload Failed"
            );
        }
    };

    return (
        <div className="bg-white p-6 rounded-xl shadow-md">

            <h2 className="text-xl font-bold mb-4">
                Upload PDF
            </h2>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) =>
                    setFile(
                        e.target.files[0]
                    )
                }
            />

            <button
                onClick={handleUpload}
                className="ml-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
                Upload
            </button>

            <p className="mt-4 text-lg">
                {message}
            </p>

        </div>
    );
}

export default UploadSection;