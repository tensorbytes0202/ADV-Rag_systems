function SourceCard({ source }) {

    return (

        <div className="border rounded-lg p-3 mb-2 bg-gray-50">

            <p>
                <strong>Document:</strong>
                {" "}
                {source.document}
            </p>

            <p>
                <strong>Chunk ID:</strong>
                {" "}
                {source.chunk_id}
            </p>

            <p>
                <strong>Vector Score:</strong>
                {" "}
                {source.vector_score.toFixed(3)}
            </p>

        </div>

    );
}

export default SourceCard;