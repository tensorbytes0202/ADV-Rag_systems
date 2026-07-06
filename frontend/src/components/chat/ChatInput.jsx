import { useState } from "react";

function ChatInput({

    onSend,

    loading

}) {

    const [text, setText] = useState("");

    const send = () => {

        if (!text.trim()) return;

        onSend(text);

        setText("");

    };

    return (

        <div className="flex gap-3 mt-6">

            <input

                type="text"

                className="flex-1 border rounded-lg p-3"

                placeholder="Ask anything..."

                value={text}

                onChange={(e) => setText(e.target.value)}

                onKeyDown={(e) => {

                    if (e.key === "Enter") {

                        send();

                    }

                }}

            />

            <button

                disabled={loading}

                onClick={send}

                className="bg-green-600 text-white px-6 rounded-lg"

            >

                {

                    loading

                        ?

                        "Thinking..."

                        :

                        "Send"

                }

            </button>

        </div>

    );

}

export default ChatInput;