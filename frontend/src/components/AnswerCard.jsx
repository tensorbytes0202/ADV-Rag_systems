import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { tomorrow } from "react-syntax-highlighter/dist/esm/styles/prism";

function AnswerCard({ answer }) {

    return (

        <div className="bg-white border rounded-xl shadow-sm p-6">

            <h2 className="text-2xl font-bold mb-6">

                Answer

            </h2>

            <div className="prose prose-lg max-w-none">

                <ReactMarkdown

                    remarkPlugins={[remarkGfm]}

                    components={{

                        code({

                            inline,

                            className,

                            children,

                            ...props

                        }) {

                            const match = /language-(\w+)/.exec(

                                className || ""

                            );

                            return !inline && match ? (

                                <div className="relative">

                                    <button

                                        onClick={() =>
                                            navigator.clipboard.writeText(
                                                String(children)
                                            )
                                        }

                                        className="absolute right-3 top-3 bg-gray-700 text-white text-xs px-3 py-1 rounded"

                                    >

                                        Copy

                                    </button>

                                    <SyntaxHighlighter

                                        style={tomorrow}

                                        language={match[1]}

                                        PreTag="div"

                                        {...props}

                                    >

                                        {String(children).replace(/\n$/, "")}

                                    </SyntaxHighlighter>

                                </div>

                            ) : (

                                <code

                                    className="bg-gray-200 px-1 rounded"

                                    {...props}

                                >

                                    {children}

                                </code>

                            );

                        }

                    }}

                >

                    {answer}

                </ReactMarkdown>

            </div>

        </div>

    );

}

export default AnswerCard;