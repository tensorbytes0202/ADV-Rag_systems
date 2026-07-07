import { useEffect, useState } from "react";

import { Document, Page, pdfjs } from "react-pdf";

import pdfWorker from "pdfjs-dist/build/pdf.worker.min.mjs?url";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = pdfWorker;

function PDFViewer({

    filename,

    initialPage = 1

}) {

    const [numPages, setNumPages] = useState(0);

    const [pageNumber, setPageNumber] = useState(initialPage);

    const [scale, setScale] = useState(1.2);

    const [error, setError] = useState("");

    useEffect(() => {

        setPageNumber(initialPage);

        setError("");

    }, [filename, initialPage]);

    if (!filename) {

        return (

            <div className="bg-white rounded-xl shadow p-6">

                <h2 className="text-xl font-bold mb-4">

                    PDF Viewer

                </h2>

                <div className="text-gray-500">

                    No document selected.

                </div>

            </div>

        );

    }

    const pdfUrl =
        `http://127.0.0.1:8000/pdf/${encodeURIComponent(filename)}`;

    console.log("================================");
    console.log("PDF URL");
    console.log(pdfUrl);
    console.log("================================");

    return (

        <div className="bg-white rounded-xl shadow p-5 h-full">

            <h2 className="text-2xl font-bold mb-5">

                PDF Viewer

            </h2>

            {/* Toolbar */}

            <div className="flex flex-wrap gap-3 mb-5">

                <button

                    onClick={() =>

                        setPageNumber(prev =>

                            Math.max(prev - 1, 1)

                        )

                    }

                    className="bg-gray-700 text-white px-4 py-2 rounded"

                >

                    ◀ Prev

                </button>

                <button

                    onClick={() =>

                        setPageNumber(prev =>

                            Math.min(prev + 1, numPages)

                        )

                    }

                    className="bg-gray-700 text-white px-4 py-2 rounded"

                >

                    Next ▶

                </button>

                <button

                    onClick={() =>

                        setScale(prev => prev + 0.2)

                    }

                    className="bg-green-600 text-white px-4 py-2 rounded"

                >

                    Zoom +

                </button>

                <button

                    onClick={() =>

                        setScale(prev =>

                            Math.max(0.6, prev - 0.2)

                        )

                    }

                    className="bg-red-600 text-white px-4 py-2 rounded"

                >

                    Zoom -

                </button>

                <input

                    type="number"

                    min={1}

                    max={numPages}

                    value={pageNumber}

                    onChange={(e) => {

                        const page = Number(e.target.value);

                        if (

                            page >= 1 &&

                            page <= numPages

                        ) {

                            setPageNumber(page);

                        }

                    }}

                    className="border rounded px-3 w-20"

                />

            </div>

            <div className="mb-4 text-lg">

                <strong>

                    Page {pageNumber}

                </strong>

                {

                    numPages > 0 &&

                    <> / {numPages}</>

                }

            </div>

            {

                error && (

                    <div className="bg-red-100 text-red-700 rounded-lg p-4 mb-4">

                        {error}

                    </div>

                )

            }

            <div className="border rounded-lg h-[850px] overflow-auto bg-gray-100 flex justify-center">

                <Document

                    key={filename}

                    file={pdfUrl}

                    loading={

                        <div className="p-10 text-lg">

                            Loading PDF...

                        </div>

                    }

                    onLoadSuccess={({ numPages }) => {

                        console.log("PDF Loaded");

                        console.log(numPages);

                        setNumPages(numPages);

                        setError("");

                    }}

                    onLoadError={(err) => {

                        console.error("========== PDF ERROR ==========");

                        console.error(err);

                        setError(err.message);

                    }}

                >

                    <Page

                        pageNumber={pageNumber}

                        scale={scale}

                    />

                </Document>

            </div>

        </div>

    );

}

export default PDFViewer;