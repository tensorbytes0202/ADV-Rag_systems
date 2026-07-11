function PipelineTimeline({ result }) {

    if (!result) return null;

    const steps = [

        {
            name: "Query Rewrite",
            status: "done"
        },

        {
            name: "Metadata Extraction",
            status: "done"
        },

        {
            name: "Dense Retrieval",
            status:
                result.retrieved_parent > 0
                    ? "done"
                    : "failed"
        },

        {
            name: "Context Expansion",
            status:
                result.retrieved_expanded > 0
                    ? "done"
                    : "failed"
        },

        {
            name: "Compression",
            status:
                result.retrieved_compressed > 0
                    ? "done"
                    : "failed"
        },

        {
            name: "LLM Generation",
            status:
                result.answer
                    ? "done"
                    : "failed"
        },

        {
            name: "Verification",
            status:
                result.verification
                    ? "done"
                    : "failed"
        }

    ];

    return (

        <div className="mt-6 bg-white rounded-xl shadow p-5">

            <h2 className="font-bold text-xl mb-5">

                Retrieval Pipeline

            </h2>

            {

                steps.map((step, index) => (

                    <div
                        key={index}
                        className="flex items-center mb-4"
                    >

                        <div
                            className={`w-8 h-8 rounded-full flex items-center justify-center text-white
                            ${step.status === "done"
                                    ? "bg-green-500"
                                    : "bg-red-500"
                                }`}
                        >

                            {
                                step.status === "done"
                                    ? "✓"
                                    : "✕"
                            }

                        </div>

                        <div className="ml-4">

                            {step.name}

                        </div>

                    </div>

                ))

            }

            {/* Verification Details */}

            {

                result.verification_reason && (

                    <div className="mt-6 border-t pt-4">

                        <h3 className="font-semibold mb-2">

                            Verification Result

                        </h3>

                        <p className="text-gray-700">

                            {result.verification_reason}

                        </p>

                        <p className="text-sm text-gray-500 mt-2">

                            Confidence:{" "}

                            {Math.round(
                                (result.verification_confidence || 0) * 100
                            )}%

                        </p>

                    </div>

                )

            }

        </div>

    );

}

export default PipelineTimeline;