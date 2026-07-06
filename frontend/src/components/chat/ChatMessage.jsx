import AnswerCard from "../AnswerCard";
import ConfidenceBar from "../ConfidenceBar";
import AnalyticsDashboard from "../AnalyticsDashboard";
import PipelineTimeline from "../PipelineTimeline";
import SourceCard from "../SourceCard";
import ChunkViewer from "../ChunkViewer";

function ChatMessage({ message }) {

    // ==========================
    // USER MESSAGE
    // ==========================

    if (message.role === "user") {

        return (

            <div className="flex justify-end mb-8">

                <div className="bg-green-600 text-white rounded-2xl px-5 py-4 max-w-3xl shadow-lg">

                    <div className="flex items-center gap-2 mb-3">

                        <div className="w-8 h-8 rounded-full bg-white text-green-600 font-bold flex items-center justify-center">

                            U

                        </div>

                        <span className="font-semibold">

                            You

                        </span>

                    </div>

                    <div className="leading-7 whitespace-pre-wrap">

                        {message.content}

                    </div>

                </div>

            </div>

        );

    }

    // ==========================
    // AI MESSAGE
    // ==========================

    return (

        <div className="flex justify-start mb-10">

            <div className="bg-white rounded-2xl shadow-lg w-full p-6">

                {/* Header */}

                <div className="flex items-center justify-between mb-6">

                    <div className="flex items-center gap-3">

                        <div className="w-12 h-12 rounded-full bg-green-600 text-white font-bold flex items-center justify-center">

                            AI

                        </div>

                        <div>

                            <h2 className="font-bold text-lg">

                                Advanced RAG Assistant

                            </h2>

                            <p className="text-sm text-gray-500">

                                Powered by Local LLM

                            </p>

                        </div>

                    </div>

                    <button

                        onClick={() =>
                            navigator.clipboard.writeText(
                                message.answer || ""
                            )
                        }

                        className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"

                    >

                        📋 Copy

                    </button>

                </div>

                {/* Answer */}

                <AnswerCard

                    answer={message.answer}

                />

                {/* Confidence */}

                <div className="mt-8">

                    <ConfidenceBar

                        confidence={message.confidence}

                    />

                </div>

                {/* Analytics */}

                <div className="mt-8">

                    <AnalyticsDashboard

                        result={message}

                    />

                </div>

                {/* Pipeline */}

                <div className="mt-8">

                    <PipelineTimeline

                        result={message}

                    />

                </div>

                {/* Sources */}

                {

                    message.sources?.length > 0 && (

                        <div className="mt-10">

                            <h2 className="text-xl font-bold mb-4">

                                📚 Sources

                            </h2>

                            {

                                message.sources.map(

                                    (source, index) => (

                                        <SourceCard

                                            key={index}

                                            source={source}

                                        />

                                    )

                                )

                            }

                        </div>

                    )

                }

                {/* Chunks */}

                {

                    message.context_chunks?.length > 0 && (

                        <div className="mt-10">

                            <ChunkViewer

                                chunks={message.context_chunks}

                            />

                        </div>

                    )

                }

                {/* Suggested Questions */}

                {

                    message.followup_questions?.length > 0 && (

                        <div className="mt-10">

                            <h2 className="text-xl font-bold mb-4">

                                💡 Suggested Questions

                            </h2>

                            <div className="space-y-3">

                                {

                                    message.followup_questions.map(

                                        (question, index) => (

                                            <button

                                                key={index}

                                                className="w-full text-left border rounded-xl p-4 hover:bg-gray-100 transition"

                                            >

                                                {question}

                                            </button>

                                        )

                                    )

                                }

                            </div>

                        </div>

                    )

                }

            </div>

        </div>

    );

}

export default ChatMessage;