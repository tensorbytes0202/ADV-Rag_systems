import { useEffect, useState } from "react";
import api from "../services/api";

function ActiveDocument({

    activeDocument,

    setActiveDocument

}) {

    const [documents, setDocuments] = useState([]);

    useEffect(() => {

        loadDocuments();

    }, []);

    const loadDocuments = async () => {

        try {

            const docs = await api.get("/documents");

            setDocuments(docs.data.documents);

            const active = await api.get(

                "/documents/active"

            );

            const currentDocument =

                active.data.active_document;

            setActiveDocument(

                currentDocument

            );

        }

        catch (err) {

            console.log(err);

        }

    };

    const changeDocument = async (

        documentName

    ) => {

        try {

            await api.post(

                `/documents/active/${documentName}`

            );

            setActiveDocument(

                documentName

            );

        }

        catch (err) {

            console.log(err);

        }

    };

    return (

        <div className="bg-white rounded-xl shadow p-6 mb-6">

            <h2 className="text-2xl font-bold mb-4">

                Active Document

            </h2>

            {

                documents.length === 0 ?

                    (

                        <p className="text-gray-500">

                            No documents uploaded.

                        </p>

                    )

                    :

                    (

                        <select

                            className="w-full border rounded-lg p-3"

                            value={activeDocument}

                            onChange={(e) =>

                                changeDocument(

                                    e.target.value

                                )

                            }

                        >

                            {

                                documents.map(

                                    (doc) => (

                                        <option

                                            key={doc.name}

                                            value={doc.name}

                                        >

                                            {doc.name}

                                            {" "}

                                            ({doc.pages} pages)

                                        </option>

                                    )

                                )

                            }

                        </select>

                    )

            }

            <div className="mt-4">

                <strong>

                    Current:

                </strong>

                {" "}

                {activeDocument || "None"}

            </div>

        </div>

    );

}

export default ActiveDocument;