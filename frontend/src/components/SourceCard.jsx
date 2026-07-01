function SourceCard({ source }) {

    return (

        <div className="border rounded-lg p-3 mb-2 bg-gray-50">

            <p>
                <strong>Document:</strong>{" "}
                {source?.document ?? "Unknown"}
            </p>

            <p>
                <strong>Page:</strong>{" "}
                {source?.page ?? "N/A"}
            </p>

            <p>
                <strong>Chunk ID:</strong>{" "}
                {source?.chunk_id ?? "N/A"}
            </p>

            <p>
                <strong>Vector Score:</strong>{" "}
                {
                    typeof source?.vector_score === "number"
                        ? source.vector_score.toFixed(3)
                        : "N/A"
                }
            </p>

        </div>

    );
}

export default SourceCard;