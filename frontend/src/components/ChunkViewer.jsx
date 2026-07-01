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
                                Rerank Score:
                                {" "}
                                {chunk.rerank_score.toFixed(2)}
                            </p>

                            {
                                chunk.page && (
                                    <p className="text-sm mt-1">
                                        Page:
                                        {" "}
                                        {chunk.page}
                                    </p>
                                )
                            }

                            {
                                chunk.document && (
                                    <p className="text-sm mt-1">
                                        Document:
                                        {" "}
                                        {chunk.document}
                                    </p>
                                )
                            }

                            <div className="mt-3 text-sm whitespace-pre-wrap">
                                {chunk.text}
                            </div>

                        </div>

                    )
                )
            }

        </div>
    );
}

export default ChunkViewer;