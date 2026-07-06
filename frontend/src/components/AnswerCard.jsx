import ReactMarkdown from "react-markdown";

function AnswerCard({ answer }) {

    return (

        <div className="bg-gray-50 border rounded-xl p-5">

            <h2 className="text-xl font-bold mb-4">

                Answer

            </h2>

            <div className="prose max-w-none">

                <ReactMarkdown>

                    {answer}

                </ReactMarkdown>

            </div>

        </div>

    );

}

export default AnswerCard;