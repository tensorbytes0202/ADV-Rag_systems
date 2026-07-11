import { useEffect, useState } from "react";

import { Document, Page, pdfjs } from "react-pdf";
import pdfWorker from "pdfjs-dist/build/pdf.worker.min.mjs?url";

import { usePDF } from "../context/PDFContext";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = pdfWorker;

function PDFViewer({

    filename: activeDocument,

    initialPage = 1

}) {

    const { pdfState } = usePDF();

    const filename =
        pdfState.filename || activeDocument;

    const [numPages, setNumPages] = useState(0);

    const [pageNumber, setPageNumber] = useState(initialPage);

    const [scale, setScale] = useState(1.2);

    const [error, setError] = useState("");

    useEffect(() => {

        if (pdfState.page) {

            setPageNumber(pdfState.page);

        } else {

            setPageNumber(initialPage);

        }

        setError("");

    }, [

        filename,

        pdfState.page,

        initialPage

    ]);

    if (!filename) {

        return (

            <div className="bg-white rounded-xl shadow p-6">

                <h2 className="text-xl font-bold mb-4">

                    PDF Viewer

                </h2>

                <p className="text-gray-500">

                    No document selected.

                </p>

            </div>

        );

    }

    const pdfUrl =
        `http://127.0.0.1:8000/pdf/${encodeURIComponent(filename)}`;

    return (

        <div className="bg-white rounded-xl shadow p-5 h-full">

            <h2 className="text-2xl font-bold mb-5">

                PDF Viewer

            </h2>

            <div className="mb-4">

                <div className="font-semibold">

                    📄 {filename}

                </div>

            </div>

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

                    value={pageNumber}

                    min={1}

                    max={numPages || 1}

                    onChange={(e) => {

                        const page = Number(e.target.value);

                        if (

                            page >= 1 &&

                            page <= numPages

                        ) {

                            setPageNumber(page);

                        }

                    }}

                    className="border rounded px-3 w-24"

                />

            </div>

            <div className="mb-4 font-semibold">

                Page {pageNumber}

                {

                    numPages > 0 &&

                    <> / {numPages}</>

                }

            </div>

            {

                error && (

                    <div className="bg-red-100 text-red-700 rounded p-4 mb-4">

                        {error}

                    </div>

                )

            }

            <div className="border rounded-lg h-[800px] overflow-auto bg-gray-100 flex justify-center">

                <Document

                    key={`${filename}-${pageNumber}`}

                    file={pdfUrl}

                    loading={

                        <div className="p-10">

                            Loading PDF...

                        </div>

                    }

                    onLoadSuccess={({ numPages }) => {

                        setNumPages(numPages);

                        setError("");

                    }}

                    onLoadError={(err) => {

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

            {/* Retrieved Chunk */}

            {

                pdfState.chunk && (

                    <div className="mt-6 bg-yellow-50 border-l-4 border-yellow-500 rounded-lg p-5">

                        <h3 className="font-bold text-lg mb-3">

                            📌 Retrieved Chunk

                        </h3>

                        <div className="whitespace-pre-wrap leading-7">

                            {pdfState.chunk}

                        </div>

                    </div>

                )

            }

            {/* Parent Context */}

            {

                pdfState.parent && (

                    <div className="mt-5 bg-blue-50 border-l-4 border-blue-500 rounded-lg p-5">

                        <h3 className="font-bold text-lg mb-3">

                            📖 Parent Context

                        </h3>

                        <div className="whitespace-pre-wrap leading-7">

                            {pdfState.parent}

                        </div>

                    </div>

                )

            }

        </div>

    );

}

export default PDFViewer;