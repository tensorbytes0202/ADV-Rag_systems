function ChunkViewer({ chunks }) {

    return (

        <div className="mt-6">

            <h3 className="text-xl font-bold mb-3">
                Retrieved Chunks
            </h3>

            {
                chunks.map(
                    (chunk, index) => (

                        <div
                            key={index}
                            className="border rounded-lg p-4 mb-3 bg-gray-50"
                        >

                            <p className="font-semibold">
                                Chunk #{index + 1}
                            </p>

                            <p className="text-sm mt-2">
                                Score:
                                {" "}
                                {chunk.rerank_score.toFixed(2)}
                            </p>

                            <p className="mt-3">
                                {chunk.text}
                            </p>

                        </div>

                    )
                )
            }

        </div>
    );
}

export default ChunkViewer;