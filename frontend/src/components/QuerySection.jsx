import { useState } from "react";
import api from "../services/api";
import SourceCard from "./SourceCard";
import ConfidenceBar from "./ConfidenceBar";
import ChunkViewer from "./ChunkViewer";
function QuerySection() {

    const [question, setQuestion] = useState("");

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);

    const handleAsk = async () => {

        if (!question) return;

        setLoading(true);

        try {

            const response = await api.post(
                "/query",
                {
                    question
                }
            );

            setResult(
                response.data
            );

        } catch (error) {

            console.log(error);

        } finally {

            setLoading(false);

        }
    };

    return (

        <div className="bg-white p-6 rounded-xl shadow-md mt-6">

            <h2 className="text-xl font-bold mb-4">
                Ask Question
            </h2>

            <input
                type="text"
                placeholder="Ask anything..."
                value={question}
                onChange={(e) =>
                    setQuestion(
                        e.target.value
                    )
                }
                className="border p-2 w-2/3 rounded"
            />

            <button
                onClick={handleAsk}
                className="ml-4 bg-green-600 text-white px-4 py-2 rounded"
            >
                Ask
            </button>

            {
                loading &&
                <p className="mt-4">
                    Thinking...
                </p>
            }

            {
                result && (

                    <div className="mt-6">

                        <h3 className="font-bold text-lg">
                            Answer
                        </h3>

                        <p className="mt-2">
                            {result.answer}
                        </p>

                        <ConfidenceBar
                            confidence={result.confidence}
                        />

                        <div className="mt-4">

                            <strong>
                                Dense Results:
                            </strong>

                            {" "}

                            {result.retrieved_dense}

                        </div>

                        <div className="mt-2">

                            <strong>
                                BM25 Results:
                            </strong>

                            {" "}

                            {result.retrieved_bm25}

                        </div>

                        <div className="mt-2">

                            <strong>
                                Hybrid Results:
                            </strong>

                            {" "}

                            {result.retrieved_hybrid}

                        </div>

                        {/* Sources Section */}

                        <div className="mt-6">

                            <h3 className="font-bold text-lg mb-3">
                                Sources
                            </h3>

                            {
                                result.sources?.map(
                                    (source, index) => (

                                        <SourceCard
                                            key={index}
                                            source={source}
                                        />

                                    )
                                )
                            }

                        </div>

                        {
                            result.context_chunks &&
                            (
                                <ChunkViewer
                                    chunks={result.context_chunks}
                                />
                            )
                        }

                    </div>

                )
            }

        </div>

    );
}

export default QuerySection;