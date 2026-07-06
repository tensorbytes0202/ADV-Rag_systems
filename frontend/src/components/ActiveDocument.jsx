import { useEffect, useState } from "react";
import api from "../services/api";

function ActiveDocument() {

    const [documents, setDocuments] = useState([]);
    const [activeDocument, setActiveDocument] = useState("");

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

            setActiveDocument(
                active.data.active_document
            );

        }

        catch (err) {

            console.log(err);

        }

    };

    const changeDocument = async (documentName) => {

        try {

            await api.post(

                `/documents/active/${documentName}`

            );

            setActiveDocument(documentName);

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

                    documents.map((doc) => (

                        <option

                            key={doc.name}

                            value={doc.name}

                        >

                            {doc.name}

                            {"  "}

                            ({doc.pages} pages)

                        </option>

                    ))

                }

            </select>

            <div className="mt-4">

                <strong>

                    Current :

                </strong>

                {" "}

                {activeDocument}

            </div>

        </div>

    );

}

export default ActiveDocument;