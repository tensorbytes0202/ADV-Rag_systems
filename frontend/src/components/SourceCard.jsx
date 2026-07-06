function SourceCard({ source }) {

    const openPDF = () => {

        const url =
            `http://127.0.0.1:8000/pdf/${source.document}#page=${source.page}`;

        window.open(url, "_blank");

    };

    return (

        <div
            className="border rounded-lg p-4 mb-3 shadow cursor-pointer hover:bg-gray-50"
            onClick={openPDF}
        >

            <h3 className="font-bold">

                {source.document}

            </h3>

            <p>

                Page : {source.page}

            </p>

            <p>

                Chunk : {source.chunk_id}

            </p>

            <p>

                Score : {source.score?.toFixed(3)}

            </p>

        </div>

    );

}

export default SourceCard;