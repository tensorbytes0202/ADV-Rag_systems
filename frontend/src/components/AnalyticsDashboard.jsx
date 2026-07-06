function AnalyticsDashboard({ result }) {

    if (!result) return null;

    const cards = [

        {
            title: "Confidence",
            value: `${Math.round(result.confidence * 100)}%`
        },

        {
            title: "Parent",
            value: result.retrieved_parent
        },

        {
            title: "Expanded",
            value: result.retrieved_expanded
        },

        {
            title: "Compressed",
            value: result.retrieved_compressed
        },

        {
            title: "BM25",
            value: result.retrieved_bm25
        },

        {
            title: "Hybrid",
            value: result.retrieved_hybrid
        },

        {
            title: "Sources",
            value: result.sources?.length || 0
        },

        {
            title: "Chunks",
            value: result.context_chunks?.length || 0
        }

    ];

    return (

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">

            {

                cards.map((card, index) => (

                    <div

                        key={index}

                        className="bg-white rounded-xl shadow-md p-5 text-center"

                    >

                        <div className="text-gray-500 text-sm">

                            {card.title}

                        </div>

                        <div className="text-3xl font-bold mt-2 text-green-600">

                            {card.value}

                        </div>

                    </div>

                ))

            }

        </div>

    );

}

export default AnalyticsDashboard;