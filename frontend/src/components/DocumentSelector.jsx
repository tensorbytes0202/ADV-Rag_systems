import { useEffect, useState } from "react";

import {
    getDocuments,
    getActiveDocument,
    setActiveDocument
} from "../services/api";

export default function DocumentSelector() {

    const [documents, setDocuments] = useState([]);

    const [activeDocument, setActive] = useState("");

    useEffect(() => {

        loadDocuments();

    }, []);

    async function loadDocuments() {

        try {

            const docs = await getDocuments();

            const active = await getActiveDocument();

            setDocuments(docs.data.documents);

            setActive(active.data.active_document);

        } catch (err) {

            console.log(err);

        }

    }

    async function handleChange(e) {

        const name = e.target.value;

        await setActiveDocument(name);

        setActive(name);

    }

    return (

        <div className="bg-white rounded-lg shadow p-5 mb-6">

            <h2 className="text-xl font-bold mb-4">

                Active Document

            </h2>

            <select

                className="border rounded p-2 w-full"

                value={activeDocument}

                onChange={handleChange}

            >

                {

                    documents.map(doc => (

                        <option

                            key={doc.name}

                            value={doc.name}

                        >

                            {doc.name}

                        </option>

                    ))

                }

            </select>

            <p className="mt-3 text-sm text-gray-600">

                Current :

                <span className="font-semibold">

                    {" "}

                    {activeDocument}

                </span>

            </p>

        </div>

    );

}