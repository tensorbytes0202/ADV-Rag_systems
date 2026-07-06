import { useChat } from "../context/ChatContext";

function Sidebar() {

    const {

        chats,

        activeChatId,

        switchChat,

        createNewChat

    } = useChat();

    return (

        <div className="w-80 h-screen bg-[#202123] text-white flex flex-col">

            {/* Header */}

            <div className="p-4 border-b border-gray-700">

                <button

                    onClick={createNewChat}

                    className="w-full bg-green-600 hover:bg-green-700 rounded-lg py-3 font-semibold"

                >

                    + New Chat

                </button>

            </div>

            {/* Chat List */}

            <div className="flex-1 overflow-y-auto p-3 space-y-2">

                {

                    chats.map(chat => (

                        <button

                            key={chat.id}

                            onClick={() => switchChat(chat.id)}

                            className={`

                                w-full

                                text-left

                                rounded-lg

                                px-4

                                py-3

                                transition

                                ${activeChatId === chat.id

                                    ?

                                    "bg-gray-700"

                                    :

                                    "hover:bg-gray-800"

                                }

                            `}

                        >

                            <div className="font-medium truncate">

                                {chat.title}

                            </div>

                            <div className="text-xs text-gray-400 mt-1">

                                {chat.messages.length} messages

                            </div>

                        </button>

                    ))

                }

            </div>

        </div>

    );

}

export default Sidebar;