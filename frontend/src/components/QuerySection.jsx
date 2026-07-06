import { useState } from "react";
import api from "../services/api";
import SourceCard from "./SourceCard";
import ConfidenceBar from "./ConfidenceBar";
import ChunkViewer from "./ChunkViewer";
import PipelineTimeline from "./PipelineTimeline";
import AnalyticsDashboard from "./AnalyticsDashboard";

function QuerySection() {

    const [question, setQuestion] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAsk = async (customQuestion = null) => {

        const finalQuestion = customQuestion || question;

        if (!finalQuestion.trim()) return;

        setLoading(true);

        try {

            const response = await api.post(
                "/query",
                {
                    question: finalQuestion
                }
            );

            console.log("========== RESPONSE ==========");
            console.log(response.data);

            console.log("========== SOURCES ==========");
            console.log(response.data.sources);

            setResult(response.data);

        } catch (error) {

            console.error("QUERY ERROR");
            console.error(error);

            if (error.response) {
                console.error(error.response.data);
            }

        } finally {

            setLoading(false);

        }

    };

    return (

        <div className="bg-white p-6 rounded-xl shadow-md mt-6">

            <h2 className="text-xl font-bold mb-4">
                Ask Question
            </h2>

            <div className="flex gap-4">

                <input
                    type="text"
                    placeholder="Ask anything..."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    className="border p-2 flex-1 rounded"
                />

                <button
                    onClick={() => handleAsk()}
                    className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
                >
                    Ask
                </button>

            </div>

            {
                loading &&
                <p className="mt-4 text-blue-600">
                    Thinking...
                </p>
            }

            {
                result && (

                    <div className="mt-8">

                        {/* Answer */}

                        <h3 className="font-bold text-2xl">
                            Answer
                        </h3>

                        <p className="mt-3 whitespace-pre-wrap leading-7">
                            {result.answer}
                        </p>

                        {/* Confidence */}

                        <div className="mt-6">

                            <ConfidenceBar
                                confidence={result.confidence}
                            />
                            <AnalyticsDashboard
                                result={result}
                            />

                        </div>

                        {/* Pipeline */}

                        <PipelineTimeline
                            result={result}
                        />

                        {/* Suggested Questions */}

                        {
                            result.followup_questions &&
                            result.followup_questions.length > 0 && (

                                <div className="mt-8">

                                    <h3 className="font-bold text-xl mb-4">

                                        Suggested Questions

                                    </h3>

                                    <div className="space-y-3">

                                        {

                                            result.followup_questions.map(

                                                (q, index) => (

                                                    <button

                                                        key={index}

                                                        onClick={() => {

                                                            setQuestion(q);

                                                            setTimeout(() => {

                                                                handleAsk(q);

                                                            }, 100);

                                                        }}

                                                        className="w-full text-left border rounded-lg p-3 hover:bg-gray-100 transition"

                                                    >

                                                        {q}

                                                    </button>

                                                )

                                            )

                                        }

                                    </div>

                                </div>

                            )
                        }

                        {/* Retrieval Statistics */}

                        <div className="mt-8 bg-gray-50 rounded-xl p-5">

                            <h3 className="font-bold text-xl mb-4">

                                Retrieval Statistics

                            </h3>

                            <div className="grid grid-cols-2 gap-4">

                                <div>

                                    <strong>Parent Results :</strong>{" "}
                                    {result.retrieved_parent}

                                </div>

                                <div>

                                    <strong>Expanded Results :</strong>{" "}
                                    {result.retrieved_expanded}

                                </div>

                                <div>

                                    <strong>Compressed Results :</strong>{" "}
                                    {result.retrieved_compressed}

                                </div>

                                <div>

                                    <strong>BM25 Results :</strong>{" "}
                                    {result.retrieved_bm25}

                                </div>

                                <div>

                                    <strong>Hybrid Results :</strong>{" "}
                                    {result.retrieved_hybrid}

                                </div>

                            </div>

                        </div>

                        {/* Sources */}

                        <div className="mt-8">

                            <h3 className="font-bold text-xl mb-4">

                                Sources

                            </h3>

                            {

                                Array.isArray(result.sources) &&

                                result.sources.map(

                                    (source, index) => (

                                        <SourceCard

                                            key={index}

                                            source={source}

                                        />

                                    )

                                )

                            }

                        </div>

                        {/* Retrieved Chunks */}

                        {

                            Array.isArray(result.context_chunks) && (

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