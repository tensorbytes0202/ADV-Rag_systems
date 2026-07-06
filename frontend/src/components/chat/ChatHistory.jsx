import { useEffect, useRef } from "react";

import { useChat } from "../../context/ChatContext";

import ChatMessage from "./ChatMessage";

function ChatHistory() {

    const {

        activeChat

    } = useChat();

    const bottomRef = useRef(null);

    const messages = activeChat?.messages || [];

    useEffect(() => {

        bottomRef.current?.scrollIntoView({

            behavior: "smooth"

        });

    }, [messages]);

    if (!activeChat) {

        return (

            <div className="text-center text-gray-500 py-10">

                No active chat found.

            </div>

        );

    }

    return (

        <div className="space-y-6">

            {

                messages.length === 0 ? (

                    <div className="text-center text-gray-400 py-16">

                        <h2 className="text-2xl font-bold mb-3">

                            👋 Welcome to Advanced RAG

                        </h2>

                        <p>

                            Ask a question about your uploaded document to start chatting.

                        </p>

                    </div>

                ) : (

                    messages.map((message) => (

                        <ChatMessage

                            key={message.id}

                            message={message}

                        />

                    ))

                )

            }

            <div ref={bottomRef}></div>

        </div>

    );

}

export default ChatHistory;