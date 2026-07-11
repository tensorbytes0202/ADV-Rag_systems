import { usePDF } from "../context/PDFContext";

function SourceCard({ source }) {

    const { openPDF } = usePDF();

    const handleClick = () => {

        openPDF(

            source.document,

            source.page,

            source.text,

            source.parent_text

        );

    };

    return (

        <div

            onClick={handleClick}

            className="border rounded-xl p-4 mb-3 shadow cursor-pointer hover:bg-blue-50 transition"

        >

            <h3 className="font-bold text-lg">

                📄 {source.document}

            </h3>

            <p className="mt-2">

                <strong>Page:</strong> {source.page}

            </p>

            {

                source.chunk_id && (

                    <p>

                        <strong>Chunk:</strong> {source.chunk_id}

                    </p>

                )

            }

            {

                source.score !== undefined && (

                    <p>

                        <strong>Score:</strong>{" "}

                        {Number(source.score).toFixed(3)}

                    </p>

                )

            }

            <div className="mt-3 text-blue-600 font-semibold">

                Click to open in PDF Viewer →

            </div>

        </div>

    );

}

export default SourceCard;