import { useState } from "react";

import api from "../../services/api";

import { useChat } from "../../context/ChatContext";

import ChatHistory from "./ChatHistory";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";

function ChatWindow() {

    const {

        addUserMessage,

        addAssistantMessage,

        activeChat

    } = useChat();

    const chat = useChat();

    console.log("CHAT CONTEXT");
    console.log(chat);

    const [loading, setLoading] = useState(false);

    const handleSend = async (question) => {

        if (!question.trim()) return;

        // ==========================
        // Add User Message
        // ==========================

        addUserMessage(question);

        setLoading(true);

        try {
            const response = await fetch(

                "http://127.0.0.1:8000/query/stream",

                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify({

                        question

                    })

                }

            );

            const reader = response.body.getReader();

            const decoder = new TextDecoder();

            let answer = "";

            while (true) {

                const { done, value } = await reader.read();

                if (done) break;

                const chunk = decoder.decode(value);

                const lines = chunk.split("\n");

                for (const line of lines) {

                    if (!line.trim()) continue;

                    const data = JSON.parse(line);

                    answer += data.token;

                }

            }

            addAssistantMessage({

                answer,

                confidence: 100,

                sources: [],

                context_chunks: [],

                followup_questions: []

            });

        }

        catch (error) {

            console.error(error);

            addAssistantMessage({

                role: "assistant",

                timestamp: new Date().toISOString(),

                answer:
                    "❌ Something went wrong while generating the answer.",

                confidence: 0,

                sources: [],

                context_chunks: [],

                followup_questions: [],

                retrieved_parent: 0,

                retrieved_expanded: 0,

                retrieved_compressed: 0,

                retrieved_bm25: 0,

                retrieved_hybrid: 0

            });

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="bg-gray-100 rounded-xl shadow-lg p-6">

            {/* Chat Header */}

            <div className="flex justify-between items-center mb-6">

                <div>

                    <h2 className="text-2xl font-bold">

                        Advanced RAG Chat

                    </h2>

                    <p className="text-gray-500">

                        Ask questions about the active document.

                    </p>

                </div>

                <div className="text-sm text-gray-500">

                    {activeChat?.messages?.length || 0} Messages

                </div>

            </div>

            {/* Conversation */}

            <ChatHistory />

            {/* Typing */}

            {

                loading &&

                <TypingIndicator />

            }

            {/* Input */}

            <div className="mt-6">

                <ChatInput

                    onSend={handleSend}

                    loading={loading}

                />

            </div>

        </div>

    );

}

export default ChatWindow;