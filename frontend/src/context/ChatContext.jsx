import { createContext, useContext, useEffect, useState } from "react";

const ChatContext = createContext();

export function ChatProvider({ children }) {

    const [chats, setChats] = useState(() => {

        const saved = localStorage.getItem("rag_chats");

        if (saved) {

            return JSON.parse(saved);

        }

        return [

            {

                id: Date.now(),

                title: "New Chat",

                createdAt: new Date().toISOString(),

                messages: []

            }

        ];

    });

    const [activeChatId, setActiveChatId] = useState(() => {

        const saved = localStorage.getItem("active_chat");

        if (saved) return Number(saved);

        return chats[0].id;

    });

    // ==========================
    // Save Automatically
    // ==========================

    useEffect(() => {

        localStorage.setItem(

            "rag_chats",

            JSON.stringify(chats)

        );

    }, [chats]);

    useEffect(() => {

        localStorage.setItem(

            "active_chat",

            activeChatId

        );

    }, [activeChatId]);

    // ==========================
    // Active Chat
    // ==========================

    const activeChat = chats.find(

        chat => chat.id === activeChatId

    );

    // ==========================
    // New Chat
    // ==========================

    const createNewChat = () => {

        const newChat = {

            id: Date.now(),

            title: "New Chat",

            createdAt: new Date().toISOString(),

            messages: []

        };

        setChats(prev => [

            newChat,

            ...prev

        ]);

        setActiveChatId(newChat.id);

    };

    // ==========================
    // Switch Chat
    // ==========================

    const switchChat = (chatId) => {

        setActiveChatId(chatId);

    };

    // ==========================
    // Delete Chat
    // ==========================

    const deleteChat = (chatId) => {

        const updated = chats.filter(

            chat => chat.id !== chatId

        );

        setChats(updated);

        if (updated.length > 0) {

            setActiveChatId(updated[0].id);

        }

    };

    // ==========================
    // Rename Chat
    // ==========================

    const renameChat = (

        chatId,

        title

    ) => {

        setChats(prev =>

            prev.map(chat =>

                chat.id === chatId

                    ? {

                        ...chat,

                        title

                    }

                    : chat

            )

        );

    };

    // ==========================
    // Add User Message
    // ==========================

    const addUserMessage = (content) => {

        const message = {

            id: Date.now(),

            role: "user",

            content,

            timestamp: new Date().toISOString()

        };

        setChats(prev =>

            prev.map(chat =>

                chat.id === activeChatId

                    ? {

                        ...chat,

                        title:

                            chat.messages.length === 0

                                ? content.slice(0, 40)

                                : chat.title,

                        messages: [

                            ...chat.messages,

                            message

                        ]

                    }

                    : chat

            )

        );

    };

    // ==========================
    // Add Assistant Message
    // ==========================

    const addAssistantMessage = (response) => {

        const message = {

            id: Date.now(),

            role: "assistant",

            timestamp: new Date().toISOString(),

            answer: response.answer,

            confidence: response.confidence,

            sources: response.sources || [],

            context_chunks:

                response.context_chunks || [],

            followup_questions:

                response.followup_questions || [],

            retrieved_parent:

                response.retrieved_parent,

            retrieved_expanded:

                response.retrieved_expanded,

            retrieved_compressed:

                response.retrieved_compressed,

            retrieved_bm25:

                response.retrieved_bm25,

            retrieved_hybrid:

                response.retrieved_hybrid,

            pipeline:

                response.pipeline || {}

        };

        setChats(prev =>

            prev.map(chat =>

                chat.id === activeChatId

                    ? {

                        ...chat,

                        messages: [

                            ...chat.messages,

                            message

                        ]

                    }

                    : chat

            )

        );

    };

    // ==========================
    // Clear Current Chat
    // ==========================

    const clearChat = () => {

        setChats(prev =>

            prev.map(chat =>

                chat.id === activeChatId

                    ? {

                        ...chat,

                        messages: []

                    }

                    : chat

            )

        );

    };

    return (

        <ChatContext.Provider

            value={{

                chats,

                activeChat,

                activeChatId,

                switchChat,

                createNewChat,

                deleteChat,

                renameChat,

                addUserMessage,

                addAssistantMessage,

                clearChat

            }}

        >

            {children}

        </ChatContext.Provider>

    );

}

export function useChat() {

    return useContext(ChatContext);

}